#!/usr/bin/env python3
"""Bulk-load questions from a JSON file (list of objects) into practice.db.

Expected keys per object: paper_q_num, part, topic, subtopic, tier, difficulty,
question_text, option_a..option_d, correct_answer, answer_status, answer_notes,
source_image. Missing keys default to NULL.
"""
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "practice.db"

FIELDS = [
    "paper_q_num", "part", "topic", "subtopic", "tier", "difficulty",
    "question_text", "option_a", "option_b", "option_c", "option_d",
    "correct_answer", "answer_status", "answer_notes", "source_image",
]


def main():
    if len(sys.argv) != 2:
        print("Usage: load_json.py <file.json>")
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text())
    conn = sqlite3.connect(DB_PATH)
    cols = ", ".join(FIELDS)
    placeholders = ", ".join("?" for _ in FIELDS)
    n = 0
    for item in data:
        values = [item.get(f) for f in FIELDS]
        conn.execute(f"INSERT INTO questions ({cols}) VALUES ({placeholders})", values)
        n += 1
    conn.commit()
    print(f"Loaded {n} questions from {sys.argv[1]}")


if __name__ == "__main__":
    main()
