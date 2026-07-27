#!/usr/bin/env python3
"""CLI practice-problem server, backed by practice/practice.db.

Never dumps the full question bank at the terminal — `next` always returns a
small batch. Run with no arguments in an interactive terminal to launch the
curses TUI (tui.py); any subcommand below still works as a scriptable
fallback, same behavior as before the TUI existed.
"""
import argparse
import sys

import ai_explain
import db


def cmd_init(args):
    conn = db.connect()
    db.init_db(conn)
    print(f"Initialized {db.DB_PATH}")


def cmd_next(args):
    conn = db.connect()
    batch = db.fetch_next_batch(conn, topic=args.topic, n=args.n)
    if not batch:
        print("No questions match." if args.topic else "Question bank is empty — run `init` first.")
        return

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
    print("Answer with: practice.py answer <id> <a|b|c|d|correct|incorrect|hint|skip>")
    print("Stuck? practice.py hint <id> [--level 2|3]   /   practice.py link <id>   /   practice.py explain <id>")


def cmd_answer(args):
    conn = db.connect()
    row = db.fetch_question(conn, args.question_id)
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
        db.record_attempt(conn, args.question_id, val, outcome)
        if outcome == "solved_cold":
            print("Correct.")
        else:
            correct_opt = row[f"option_{row['correct_answer']}"]
            print(f"Incorrect. Correct answer: ({row['correct_answer']}) {correct_opt}")
            if row["answer_notes"]:
                print(f"Note: {row['answer_notes']}")
    elif val in ("correct", "incorrect"):
        outcome = "solved_cold" if val == "correct" else "wrong"
        db.record_attempt(conn, args.question_id, None, outcome, notes="self-reported")
        print(f"Logged as {outcome} (self-reported).")
    elif val in ("hint", "skip"):
        outcome = "needed_hint" if val == "hint" else "skipped"
        db.record_attempt(conn, args.question_id, None, outcome)
        print(f"Logged as {outcome}.")
    else:
        print("Value must be one of: a b c d correct incorrect hint skip")


def cmd_hint(args):
    conn = db.connect()
    row = db.fetch_question(conn, args.question_id)
    if row is None:
        print(f"No question #{args.question_id}")
        return
    level = max(1, min(3, args.level))
    hints = db.fetch_hints(conn, args.question_id, level)
    if not hints:
        print(f"No hints on file for #{args.question_id}.")
        return
    for h in hints:
        print(f"Hint {h['hint_order']}: {h['hint_text']}")
    if level < 3 and len(hints) == level:
        print(f"(Re-run with --level {level + 1} for the next hint.)")


def cmd_link(args):
    conn = db.connect()
    row = db.fetch_question(conn, args.question_id)
    if row is None:
        print(f"No question #{args.question_id}")
        return
    link = db.fetch_link(conn, row["topic"])
    if not link:
        print(f"No reference link on file for topic '{row['topic']}'.")
        return
    print(f"{row['topic']}: {link['link']}")


def cmd_explain(args):
    conn = db.connect()
    row = db.fetch_question(conn, args.question_id)
    if row is None:
        print(f"No question #{args.question_id}")
        return
    cached = None if args.refresh else db.fetch_ai_explanation(conn, args.question_id)
    if cached:
        print(cached["explanation"])
        return
    print("Asking Claude (few seconds)...")
    hints = db.fetch_hints(conn, args.question_id, level=3)
    try:
        explanation = ai_explain.generate(row, hints)
    except ai_explain.ExplainError as e:
        print(f"Could not get an explanation: {e}")
        return
    db.save_ai_explanation(conn, args.question_id, explanation, ai_explain.MODEL)
    print(explanation)


def cmd_stats(args):
    conn = db.connect()
    rows = db.fetch_stats(conn, topic=args.topic)
    if not rows:
        print("No data.")
        return
    width = max(len(r["topic"]) for r in rows)
    width = max(width, len("Topic")) + 2
    print(f"{'Topic':<{width}}{'Total':>7}{'Attempted':>11}{'Cold':>7}{'Wrong':>7}{'Hint':>7}{'Skip':>7}")
    for r in rows:
        print(f"{r['topic']:<{width}}{r['total']:>7}{r['attempted'] or 0:>11}{r['solved_cold'] or 0:>7}"
              f"{r['wrong'] or 0:>7}{r['needed_hint'] or 0:>7}{r['skipped'] or 0:>7}")


def main():
    if len(sys.argv) == 1:
        import tui
        if tui.available():
            tui.run()
            return
        print("Not an interactive terminal -- use a subcommand instead (practice.py -h).")
        return

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

    p_hint = sub.add_parser("hint", help="Show stored hint(s) for a question")
    p_hint.add_argument("question_id", type=int)
    p_hint.add_argument("--level", type=int, default=1, help="Reveal hints 1..level (default 1)")

    p_link = sub.add_parser("link", help="Show the topic reference link for a question")
    p_link.add_argument("question_id", type=int)

    p_explain = sub.add_parser("explain", help="Get (and cache) an AI-generated explanation for a question")
    p_explain.add_argument("question_id", type=int)
    p_explain.add_argument("--refresh", action="store_true", help="Regenerate even if already cached")

    args = parser.parse_args()
    {
        "init": cmd_init, "next": cmd_next, "answer": cmd_answer, "stats": cmd_stats,
        "hint": cmd_hint, "link": cmd_link, "explain": cmd_explain,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
