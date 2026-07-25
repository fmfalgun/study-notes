#!/usr/bin/env python3
"""CLI practice-problem server, backed by practice/practice.db.

Never dumps the full question bank at the terminal — `next` always returns a
small batch. See practice/README.md for the workflow.
"""
import argparse
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


def cmd_init(args):
    conn = connect()
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    print(f"Initialized {DB_PATH}")


def _last_outcome_map(conn):
    rows = conn.execute(
        """
        SELECT question_id, outcome, attempted_at
        FROM attempts
        ORDER BY attempted_at ASC
        """
    ).fetchall()
    last = {}
    counts = {}
    for r in rows:
        last[r["question_id"]] = r["outcome"]
        counts[r["question_id"]] = counts.get(r["question_id"], 0) + 1
    return last, counts


def cmd_next(args):
    conn = connect()
    q = "SELECT * FROM questions WHERE 1=1"
    params = []
    if args.topic:
        q += " AND topic LIKE ?"
        params.append(f"%{args.topic}%")
    rows = conn.execute(q, params).fetchall()
    if not rows:
        print("No questions match." if args.topic else "Question bank is empty — run `load` first.")
        return

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

    rows = sorted(rows, key=score)
    batch = rows[: args.n]

    for row in batch:
        print(f"[#{row['id']}] {row['topic']}" + (f" — {row['subtopic']}" if row["subtopic"] else ""))
        print(f"    Tier {row['tier']} · {row['difficulty']} · Part {row['part']}"
              + (f" · Q{row['paper_q_num']}" if row['paper_q_num'] else ""))
        print(f"    {row['question_text']}")
        for letter in "abcd":
            opt = row[f"option_{letter}"]
            if opt:
                print(f"      ({letter}) {opt}")
        print()
    print(f"Answer with: practice.py answer <id> <a|b|c|d|correct|incorrect|hint|skip>")


def cmd_answer(args):
    conn = connect()
    row = conn.execute("SELECT * FROM questions WHERE id = ?", (args.question_id,)).fetchone()
    if row is None:
        print(f"No question #{args.question_id}")
        return

    val = args.value.lower()
    if val in ("a", "b", "c", "d"):
        if not row["correct_answer"]:
            print("No verified answer on file for this question.")
            print(f"Re-run as: practice.py answer {args.question_id} correct   (or) incorrect")
            return
        outcome = "solved_cold" if val == row["correct_answer"] else "wrong"
        conn.execute(
            "INSERT INTO attempts (question_id, selected_answer, outcome) VALUES (?, ?, ?)",
            (args.question_id, val, outcome),
        )
        conn.commit()
        if outcome == "solved_cold":
            print("Correct.")
        else:
            correct_opt = row[f"option_{row['correct_answer']}"]
            print(f"Incorrect. Correct answer: ({row['correct_answer']}) {correct_opt}")
            if row["answer_notes"]:
                print(f"Note: {row['answer_notes']}")
    elif val in ("correct", "incorrect"):
        outcome = "solved_cold" if val == "correct" else "wrong"
        conn.execute(
            "INSERT INTO attempts (question_id, selected_answer, outcome, notes) VALUES (?, NULL, ?, ?)",
            (args.question_id, outcome, "self-reported"),
        )
        conn.commit()
        print(f"Logged as {outcome} (self-reported).")
    elif val in ("hint", "skip"):
        outcome = "needed_hint" if val == "hint" else "skipped"
        conn.execute(
            "INSERT INTO attempts (question_id, selected_answer, outcome) VALUES (?, NULL, ?)",
            (args.question_id, outcome),
        )
        conn.commit()
        print(f"Logged as {outcome}.")
    else:
        print("Value must be one of: a b c d correct incorrect hint skip")


def cmd_stats(args):
    conn = connect()
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
    if args.topic:
        q += " WHERE q.topic LIKE ?"
        params.append(f"%{args.topic}%")
    q += " GROUP BY q.topic ORDER BY q.topic"
    rows = conn.execute(q, params).fetchall()
    if not rows:
        print("No data.")
        return
    print(f"{'Topic':<32}{'Total':>7}{'Attempted':>11}{'Cold':>7}{'Wrong':>7}{'Hint':>7}{'Skip':>7}")
    for r in rows:
        print(f"{r['topic']:<32}{r['total']:>7}{r['attempted'] or 0:>11}{r['solved_cold'] or 0:>7}"
              f"{r['wrong'] or 0:>7}{r['needed_hint'] or 0:>7}{r['skipped'] or 0:>7}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create the database from schema.sql")

    p_next = sub.add_parser("next", help="Serve the next small batch of questions")
    p_next.add_argument("--n", type=int, default=3)
    p_next.add_argument("--topic", type=str, default=None)

    p_answer = sub.add_parser("answer", help="Log the outcome for a question")
    p_answer.add_argument("question_id", type=int)
    p_answer.add_argument("value", type=str)

    p_stats = sub.add_parser("stats", help="Print progress stats")
    p_stats.add_argument("--topic", type=str, default=None)

    args = parser.parse_args()
    {"init": cmd_init, "next": cmd_next, "answer": cmd_answer, "stats": cmd_stats}[args.cmd](args)


if __name__ == "__main__":
    main()
