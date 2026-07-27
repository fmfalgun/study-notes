"""Shared DB logic for practice.py (argparse CLI) and tui.py (curses UI) --
neither talks to sqlite3 directly; both call these functions so the ranking/
scoring rules and query shapes live in exactly one place."""
import json
import random
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "practice.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

TIER_RANK = {"1": 0, "2": 1, "3": 2, "shadow": 3}
DIFF_RANK = {"Complex": 0, "Medium": 1, "Easy": 2}
OUTCOME_RANK = {None: 0, "wrong": 0, "needed_hint": 1, "skipped": 2, "solved_cold": 5}


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()


def _last_outcome_map(conn):
    rows = conn.execute(
        "SELECT question_id, outcome, attempted_at FROM attempts ORDER BY attempted_at ASC"
    ).fetchall()
    last, counts = {}, {}
    for r in rows:
        last[r["question_id"]] = r["outcome"]
        counts[r["question_id"]] = counts.get(r["question_id"], 0) + 1
    return last, counts


def fetch_next_batch(conn, topic=None, n=3):
    q = "SELECT * FROM questions WHERE 1=1"
    params = []
    if topic:
        q += " AND topic LIKE ?"
        params.append(f"%{topic}%")
    rows = conn.execute(q, params).fetchall()
    if not rows:
        return []
    last, counts = _last_outcome_map(conn)

    def score(row):
        outcome = last.get(row["id"])
        return (
            OUTCOME_RANK.get(outcome, 0),
            TIER_RANK.get(row["tier"], 4),
            DIFF_RANK.get(row["difficulty"], 3),
            counts.get(row["id"], 0),
            random.random(),
        )

    return sorted(rows, key=score)[:n]


def fetch_question(conn, question_id):
    return conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()


def record_attempt(conn, question_id, selected_answer, outcome, notes=None):
    conn.execute(
        "INSERT INTO attempts (question_id, selected_answer, outcome, notes) VALUES (?, ?, ?, ?)",
        (question_id, selected_answer, outcome, notes),
    )
    conn.commit()


def fetch_hints(conn, question_id, level=3):
    level = max(1, min(3, level))
    return conn.execute(
        "SELECT hint_order, hint_text FROM hints WHERE question_id = ? AND hint_order <= ? ORDER BY hint_order",
        (question_id, level),
    ).fetchall()


def fetch_link(conn, topic):
    return conn.execute("SELECT link FROM topic_links WHERE topic = ?", (topic,)).fetchone()


def fetch_ai_explanation(conn, question_id):
    return conn.execute(
        "SELECT explanation, model, created_at FROM ai_explanations WHERE question_id = ?",
        (question_id,),
    ).fetchone()


def save_ai_explanation(conn, question_id, explanation, model):
    conn.execute(
        "INSERT INTO ai_explanations (question_id, explanation, model) VALUES (?, ?, ?) "
        "ON CONFLICT(question_id) DO UPDATE SET "
        "explanation = excluded.explanation, model = excluded.model, created_at = CURRENT_TIMESTAMP",
        (question_id, explanation, model),
    )
    conn.commit()


def load_session_state(conn):
    return conn.execute("SELECT topic, batch_ids FROM session_state WHERE id = 1").fetchone()


def save_session_state(conn, topic, ids):
    conn.execute(
        "INSERT INTO session_state (id, topic, batch_ids) VALUES (1, ?, ?) "
        "ON CONFLICT(id) DO UPDATE SET topic = excluded.topic, batch_ids = excluded.batch_ids",
        (topic, json.dumps(ids)),
    )
    conn.commit()


def clear_session_state(conn):
    conn.execute("DELETE FROM session_state WHERE id = 1")
    conn.commit()


def delete_last_attempt(conn, question_id):
    """Undo the most recent attempt logged for a question. Returns False if
    there was nothing to undo."""
    row = conn.execute(
        "SELECT id FROM attempts WHERE question_id = ? ORDER BY attempted_at DESC, id DESC LIMIT 1",
        (question_id,),
    ).fetchone()
    if row is None:
        return False
    conn.execute("DELETE FROM attempts WHERE id = ?", (row["id"],))
    conn.commit()
    return True


def fetch_stats(conn, topic=None):
    q = """
        SELECT
            q.topic,
            COUNT(DISTINCT q.id) AS total,
            COUNT(DISTINCT a.question_id) AS attempted,
            SUM(CASE WHEN a.outcome = 'solved_cold' THEN 1 ELSE 0 END) AS solved_cold,
            SUM(CASE WHEN a.outcome = 'wrong' THEN 1 ELSE 0 END) AS wrong,
            SUM(CASE WHEN a.outcome = 'needed_hint' THEN 1 ELSE 0 END) AS needed_hint,
            SUM(CASE WHEN a.outcome = 'skipped' THEN 1 ELSE 0 END) AS skipped
        FROM questions q
        LEFT JOIN attempts a ON a.question_id = q.id
    """
    params = []
    if topic:
        q += " WHERE q.topic LIKE ?"
        params.append(f"%{topic}%")
    q += " GROUP BY q.topic ORDER BY q.topic"
    return conn.execute(q, params).fetchall()
