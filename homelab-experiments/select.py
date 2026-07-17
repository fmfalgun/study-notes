#!/usr/bin/env python3
"""
Interactive machine -> category -> topic selector for the homelab-experiments menus.

Flow: pick a machine, pick a category within that machine's markdown, pick a topic
within that category. Prints the full selected topic block (title, description,
reference link) plus context, ready to hand to an AI to research and turn into a
detailed task-plan markdown.

Non-interactive use (e.g. from an AI session) is also supported via flags:
    select.py --machine rpi5 --category "Operating Systems" --topic "Deadlock Simulator"
    select.py --list                      # dump the full machine/category/topic tree
"""

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

MACHINES = {
    "rpi5": ("Raspberry Pi 5 — CS-Engineering", HERE / "rpi5-cs-eng.md"),
    "probook": ("HP ProBook 445 G11 — Cybersecurity", HERE / "probook-cybersec.md"),
    "proone": ("HP ProOne 440 G9 — DS/AI", HERE / "proone-dsai.md"),
    "garuda": ("Garuda main machine — GPU overflow", HERE / "garuda-gpu.md"),
}

CATEGORY_RE = re.compile(r"^##\s+(.+?)\s*$")
TOPIC_RE = re.compile(r"^-\s+\*\*(.+?)\*\*\s*—\s*(.+)$")


def parse_file(path: Path):
    """Return {category: [(title, body_line), ...]} preserving order."""
    categories = {}
    current = None
    for line in path.read_text().splitlines():
        m = CATEGORY_RE.match(line)
        if m:
            current = m.group(1).strip()
            categories[current] = []
            continue
        m = TOPIC_RE.match(line)
        if m and current is not None:
            title, body = m.group(1).strip(), m.group(2).strip()
            categories[current].append((title, body))
    return categories


def choose(prompt, options):
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input(f"{prompt} [1-{len(options)}]: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Invalid choice, try again.")


def fuzzy_find(name, options):
    """Case-insensitive substring match; returns exact key if found, else None."""
    low = name.lower()
    for opt in options:
        if opt.lower() == low:
            return opt
    for opt in options:
        if low in opt.lower():
            return opt
    return None


def print_selected(machine_key, category, title, body):
    machine_label, _ = MACHINES[machine_key]
    print("\n" + "=" * 70)
    print(f"Machine : {machine_label}")
    print(f"Category: {category}")
    print(f"Topic   : {title}")
    print("-" * 70)
    print(f"{title} — {body}")
    print("=" * 70)
    print(
        "\nHand this block (machine, category, topic, description, reference link)\n"
        "to the AI along with README.md so it can research the reference link and\n"
        "your own input, then write the detailed task-plan markdown."
    )


def list_all():
    for key, (label, path) in MACHINES.items():
        print(f"\n# {key} — {label}")
        cats = parse_file(path)
        for cat, topics in cats.items():
            print(f"  ## {cat}")
            for title, _ in topics:
                print(f"    - {title}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--machine", help="machine key: rpi5 | probook | proone | garuda")
    ap.add_argument("--category", help="category name (substring match ok)")
    ap.add_argument("--topic", help="topic title (substring match ok)")
    ap.add_argument("--list", action="store_true", help="dump the full tree and exit")
    args = ap.parse_args()

    if args.list:
        list_all()
        return

    # Machine
    machine_key = args.machine
    if machine_key:
        machine_key = fuzzy_find(machine_key, MACHINES.keys())
        if not machine_key:
            sys.exit(f"Unknown machine '{args.machine}'. Options: {list(MACHINES)}")
    else:
        print("Select a machine:")
        labels = [f"{k} — {v[0]}" for k, v in MACHINES.items()]
        chosen = choose("Machine", labels)
        machine_key = chosen.split(" — ")[0]

    categories = parse_file(MACHINES[machine_key][1])

    # Category
    cat_name = args.category
    if cat_name:
        cat_name = fuzzy_find(cat_name, categories.keys())
        if not cat_name:
            sys.exit(f"Unknown category '{args.category}'. Options: {list(categories)}")
    else:
        print("\nSelect a category:")
        cat_name = choose("Category", list(categories.keys()))

    topics = categories[cat_name]

    # Topic
    topic_title = args.topic
    if topic_title:
        match = fuzzy_find(topic_title, [t for t, _ in topics])
        if not match:
            sys.exit(f"Unknown topic '{args.topic}'. Options: {[t for t, _ in topics]}")
        title, body = next(t for t in topics if t[0] == match)
    else:
        print("\nSelect a topic:")
        titles = [t for t, _ in topics]
        chosen_title = choose("Topic", titles)
        title, body = next(t for t in topics if t[0] == chosen_title)

    print_selected(machine_key, cat_name, title, body)


if __name__ == "__main__":
    main()
