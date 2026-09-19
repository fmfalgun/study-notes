"""Curses TUI for practice.py's interactive loop -- takes UX inspiration
from ../web-scrap's ig_scraper/tui.py (persistent header/footer
Screen, pick_one arrow/vim-key picker, colored rows) and
../iot-proxy-recon's cam-finder-v3.py (scrollable list navigation).

Much simpler than ig_scraper's version: practice.py has no background
work (no scrapes, no forked workers, no live log stream), just synchronous
sqlite3 reads/writes via db.py, so there's no log pane and no
multiprocessing -- every draw is a plain, blocking redraw-and-getch loop.

Falls back to practice.py's plain subcommands whenever stdin/stdout isn't a
real interactive terminal -- see available()/run() and practice.py's main().
"""
import curses
import json
import sys

import ai_explain
import db

HEADER_ROWS = 2
FOOTER_ROWS = 2

COLOR_SELECTED = 1
COLOR_HEADER = 2
COLOR_DIM = 3
COLOR_GOOD = 4
COLOR_BAD = 5


def available():
    return sys.stdin.isatty() and sys.stdout.isatty()


def run():
    return curses.wrapper(_curses_main)


class Back(Exception):
    """Esc -- step back to the previous stage."""


class Quit(Exception):
    """'Q' -- exit the whole TUI."""


class Screen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.header_text = ""
        self._init_colors()
        curses.curs_set(0)
        stdscr.keypad(True)

    def _init_colors(self):
        try:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(COLOR_SELECTED, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(COLOR_HEADER, curses.COLOR_YELLOW, -1)
            curses.init_pair(COLOR_DIM, curses.COLOR_WHITE, -1)
            curses.init_pair(COLOR_GOOD, curses.COLOR_GREEN, -1)
            curses.init_pair(COLOR_BAD, curses.COLOR_RED, -1)
            self._color = True
        except curses.error:
            self._color = False

    def attr(self, pair, extra=0):
        if not self._color:
            return extra
        return curses.color_pair(pair) | extra

    def set_header(self, text):
        self.header_text = text

    def layout(self):
        h, w = self.stdscr.getmaxyx()
        body_top = HEADER_ROWS
        body_h = max(3, h - HEADER_ROWS - FOOTER_ROWS)
        footer_row = h - 1
        return h, w, body_top, body_h, footer_row

    def addstr(self, y, x, text, attr=0):
        h, w = self.stdscr.getmaxyx()
        if y < 0 or y >= h or x >= w:
            return
        text = str(text)[: max(0, w - x - 1)]
        try:
            self.stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass

    def frame(self, help_text):
        h, w, body_top, body_h, footer_row = self.layout()
        self.stdscr.erase()
        self.addstr(0, 0, self.header_text, self.attr(COLOR_HEADER, curses.A_BOLD))
        self.addstr(1, 0, "-" * (w - 1), self.attr(COLOR_DIM, curses.A_DIM))
        self.addstr(footer_row, 0, help_text, self.attr(COLOR_DIM, curses.A_DIM))


def _global_key(key):
    if key == 27:
        raise Back()
    if key in (ord("Q"), ord("q")):
        raise Quit()
    return False


def _wrap(text, width):
    """Greedy word-wrap -- curses addstr doesn't wrap on its own."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines or [""]


def pick_one(screen, title, items, formatter=str, help_suffix=""):
    """Arrow/j-k picker. Enter confirms, Esc raises Back, Q raises Quit."""
    cursor = 0
    scroll = 0
    n = len(items)
    while True:
        h, w, body_top, body_h, footer_row = screen.layout()
        screen.frame(f"up/down or j/k: move  enter: select  esc: back  Q: quit{help_suffix}")
        screen.addstr(body_top, 0, title, screen.attr(COLOR_HEADER, curses.A_BOLD))
        list_top = body_top + 2
        list_h = max(1, body_h - 2)

        if cursor < scroll:
            scroll = cursor
        elif cursor >= scroll + list_h:
            scroll = cursor - list_h + 1

        for i in range(list_h):
            idx = scroll + i
            if idx >= n:
                break
            attr = screen.attr(COLOR_SELECTED, curses.A_BOLD) if idx == cursor else 0
            screen.addstr(list_top + i, 0, formatter(items[idx]), attr)
        screen.stdscr.refresh()

        key = screen.stdscr.getch()
        _global_key(key)
        if key in (curses.KEY_UP, ord("k")):
            cursor = max(0, cursor - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            cursor = min(n - 1, cursor + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            return cursor


def confirm(screen, question, default=True):
    value = default
    while True:
        h, w, body_top, body_h, footer_row = screen.layout()
        screen.frame("left/right or y/n: choose  enter: confirm  Q: quit")
        screen.addstr(body_top, 0, question, screen.attr(COLOR_HEADER, curses.A_BOLD))
        yes_attr = screen.attr(COLOR_SELECTED, curses.A_BOLD) if value else 0
        no_attr = screen.attr(COLOR_SELECTED, curses.A_BOLD) if not value else 0
        screen.addstr(body_top + 2, 0, "[ Yes ]", yes_attr)
        screen.addstr(body_top + 2, 10, "[ No ]", no_attr)
        screen.stdscr.refresh()

        key = screen.stdscr.getch()
        _global_key(key)
        if key in (curses.KEY_LEFT, curses.KEY_RIGHT, ord("h"), ord("l"), 9):
            value = not value
        elif key in (ord("y"), ord("Y")):
            return True
        elif key in (ord("n"), ord("N")):
            return False
        elif key in (curses.KEY_ENTER, 10, 13):
            return value


def show_lines(screen, title, lines, help_extra=""):
    """Scrollable read-only text view -- used for the stats screen."""
    scroll = 0
    while True:
        h, w, body_top, body_h, footer_row = screen.layout()
        screen.frame(f"up/down: scroll  any other key: back  Q: quit{help_extra}")
        screen.addstr(body_top, 0, title, screen.attr(COLOR_HEADER, curses.A_BOLD))
        view_top = body_top + 2
        view_h = max(1, body_h - 2)
        max_scroll = max(0, len(lines) - view_h)
        scroll = min(scroll, max_scroll)
        for i, line in enumerate(lines[scroll:scroll + view_h]):
            screen.addstr(view_top + i, 0, line)
        screen.stdscr.refresh()

        key = screen.stdscr.getch()
        if key == ord("Q"):
            raise Quit()
        if key == curses.KEY_UP:
            scroll = max(0, scroll - 1)
        elif key == curses.KEY_DOWN:
            scroll = min(max_scroll, scroll + 1)
        else:
            return


def prompt_text(screen, label):
    """Blocking single-line text input on the footer row. Enter submits
    (blank allowed), Esc cancels and returns None."""
    h, w, body_top, body_h, footer_row = screen.layout()
    buf = ""
    curses.curs_set(1)
    try:
        while True:
            line = (label + buf)[: max(0, w - 1)]
            screen.addstr(footer_row, 0, line + " " * max(0, w - 1 - len(line)))
            screen.stdscr.move(footer_row, min(w - 1, len(label) + len(buf)))
            screen.stdscr.refresh()
            ch = screen.stdscr.get_wch()
            if isinstance(ch, str):
                if ch in ("\n", "\r"):
                    return buf.strip()
                if ch == "\x1b":
                    return None
                if ch in ("\x7f", "\b"):
                    buf = buf[:-1]
                elif ch.isprintable():
                    buf += ch
            else:
                if ch == curses.KEY_ENTER:
                    return buf.strip()
                if ch == curses.KEY_BACKSPACE:
                    buf = buf[:-1]
    finally:
        curses.curs_set(0)


def _current_stage(hint_level, show_link):
    if hint_level > 0:
        return f"hint{hint_level}"
    if show_link:
        return "link"
    return "cold"


def _question_lines(row, w, revealed_hints, show_link, link_row, thread, feedback):
    lines = []
    sub = f" — {row['subtopic']}" if row["subtopic"] else ""
    lines.append(f"[#{row['id']}] {row['topic']}{sub}")
    tag = f"Tier {row['tier']} · {row['difficulty']} · Part {row['part']}"
    if row["paper_q_num"]:
        tag += f" · Q{row['paper_q_num']}"
    lines.append(tag)
    lines.append("")
    for wline in _wrap(row["question_text"], w - 1):
        lines.append(wline)
    lines.append("")
    for letter in "abcd":
        opt = row[f"option_{letter}"]
        if opt:
            for j, wline in enumerate(_wrap(f"({letter}) {opt}", w - 5)):
                prefix = "  " if j == 0 else "    "
                lines.append(prefix + wline)
    if revealed_hints:
        lines.append("")
        for h in revealed_hints:
            for j, wline in enumerate(_wrap(f"Hint {h['hint_order']}: {h['hint_text']}", w - 1)):
                lines.append(wline)
    if show_link:
        lines.append("")
        if link_row:
            lines.append(f"Link: {link_row['link']}")
        else:
            lines.append("(No reference link on file for this topic.)")
    if thread:
        lines.append("")
        for t in thread:
            who = "You" if t["role"] == "user" else "AI"
            prefix = f"[{t['stage']}] {who}: "
            for wline in _wrap(prefix + t["message"], w - 1):
                lines.append(wline)
    if feedback:
        lines.append("")
        lines.append(feedback)
    return lines


def question_view(screen, conn, row):
    """One question's interactive detail view. Returns when the user has
    answered/skipped it (auto-advances the caller to the next in batch) or
    raises Back/Quit if they bail out early via Esc/Q."""
    curses.flushinp()  # discard any buffered keystrokes so this question always
                        # waits for a deliberate fresh keypress, not a stray repeat
                        # left over from dismissing the previous one
    hint_level = 0
    show_link = False
    feedback = None
    scroll = 0
    while True:
        h, w, body_top, body_h, footer_row = screen.layout()
        screen.set_header(f"practice.py -- #{row['id']}  ({row['topic']})")
        hints = db.fetch_hints(conn, row["id"], hint_level) if hint_level else []
        link_row = db.fetch_link(conn, row["topic"]) if show_link else None
        thread = db.fetch_ai_thread(conn, row["id"])
        lines = _question_lines(row, w, hints, show_link, link_row, thread, feedback)

        if row["correct_answer"]:
            help_text = "a/b/c/d: answer  h: hint  l: link  e: explain  s: skip  esc: back to menu  Q: quit"
        else:
            help_text = "1: mark correct  2: mark incorrect  (self-report, no verified answer)  h/l/e/s/esc/Q as usual"
        if feedback:
            help_text = "u: undo this answer  any other key: next question  Q: quit"
        screen.frame(help_text)
        view_h = max(1, body_h)
        max_scroll = max(0, len(lines) - view_h)
        scroll = min(scroll, max_scroll)
        for i, line in enumerate(lines[scroll:scroll + view_h]):
            attr = 0
            if feedback and line == feedback:
                attr = screen.attr(COLOR_BAD if line.startswith("Incorrect") else COLOR_GOOD, curses.A_BOLD)
            screen.addstr(body_top + i, 0, line, attr)
        screen.stdscr.refresh()

        key = screen.stdscr.getch()
        if key == ord("Q"):
            raise Quit()

        if feedback:
            if key in (ord("u"), ord("U")):
                db.delete_last_attempt(conn, row["id"])
                feedback = None
                curses.flushinp()
                continue  # re-show the same question, undone, for a fresh answer
            return  # any other key advances past a just-answered question

        if key == 27:
            raise Back()
        elif key == curses.KEY_UP:
            scroll = max(0, scroll - 1)
        elif key == curses.KEY_DOWN:
            scroll = min(max_scroll, scroll + 1)
        elif key in (ord("h"), ord("H")):
            if hint_level < 3:
                hint_level += 1
        elif key in (ord("l"), ord("L")):
            show_link = not show_link
        elif key in (ord("e"), ord("E")):
            query = prompt_text(screen, "Ask (blank = general explanation, esc = cancel)> ")
            curses.flushinp()
            if query is not None:
                stage = _current_stage(hint_level, show_link)
                screen.addstr(footer_row, 0, "Asking Claude (few seconds)...",
                              screen.attr(COLOR_DIM, curses.A_DIM))
                screen.stdscr.refresh()
                all_hints = db.fetch_hints(conn, row["id"], level=3)
                try:
                    answer = ai_explain.ask(row, all_hints, thread, query)
                    db.append_ai_message(conn, row["id"], stage, "user", query or ai_explain.DEFAULT_QUERY)
                    db.append_ai_message(conn, row["id"], stage, "assistant", answer)
                except ai_explain.ExplainError as err:
                    feedback_line = f"(AI ask failed: {err})"
                    screen.addstr(footer_row, 0, feedback_line[: max(0, w - 1)],
                                  screen.attr(COLOR_BAD, curses.A_BOLD))
                    screen.stdscr.refresh()
                    screen.stdscr.getch()
        elif key in (ord("s"), ord("S")):
            db.record_attempt(conn, row["id"], None, "skipped")
            feedback = "Skipped."
        elif not row["correct_answer"] and key in (ord("1"), ord("2")):
            outcome = "solved_cold" if key == ord("1") else "wrong"
            db.record_attempt(conn, row["id"], None, outcome, notes="self-reported")
            feedback = f"Logged as {outcome} (self-reported)."
        elif row["correct_answer"] and 0 <= key < 256 and chr(key).lower() in "abcd":
            val = chr(key).lower()
            outcome = "solved_cold" if val == row["correct_answer"] else "wrong"
            db.record_attempt(conn, row["id"], val, outcome)
            if outcome == "solved_cold":
                feedback = "Correct."
            else:
                correct_opt = row[f"option_{row['correct_answer']}"]
                feedback = f"Incorrect. Correct answer: ({row['correct_answer']}) {correct_opt}"
                if row["answer_notes"]:
                    feedback += f"  Note: {row['answer_notes']}"


def _start_batch(conn, topic):
    """Fetch a fresh batch and persist it as the resume point. Returns the
    list of question ids, or None if the bank/topic has nothing to serve."""
    batch = db.fetch_next_batch(conn, topic=topic, n=3)
    if not batch:
        return None
    ids = [r["id"] for r in batch]
    db.save_session_state(conn, topic, ids)
    return ids


def run_batch(screen, conn, topic=None):
    """Runs one question at a time from a persisted batch. The current
    question is only dropped from session_state -- and a new one pulled --
    once it's been answered or skipped, so quitting/relaunching mid-question
    resumes on the exact same question instead of drawing a fresh batch."""
    state = db.load_session_state(conn)
    if state is not None and state["topic"] == topic:
        ids = json.loads(state["batch_ids"])
    else:
        db.clear_session_state(conn)
        ids = _start_batch(conn, topic)
        if ids is None:
            show_lines(screen, "Practice", ["No questions match." if topic else
                                             "Question bank is empty -- run practice.py init/load first."])
            return

    while True:
        row = db.fetch_question(conn, ids[0])
        try:
            question_view(screen, conn, row)
        except Back:
            return  # session_state still points at this same question

        ids.pop(0)
        if ids:
            db.save_session_state(conn, topic, ids)
            continue

        db.clear_session_state(conn)
        if not confirm(screen, "Batch done -- get another batch of 3?"):
            return
        ids = _start_batch(conn, topic)
        if ids is None:
            show_lines(screen, "Practice", ["No questions match." if topic else
                                             "Question bank is empty -- run practice.py init/load first."])
            return


def run_stats(screen, conn):
    rows = db.fetch_stats(conn)
    if not rows:
        show_lines(screen, "Stats", ["No data."])
        return
    width = max(len(r["topic"]) for r in rows)
    width = max(width, len("Topic")) + 2
    lines = [f"{'Topic':<{width}}{'Total':>7}{'Attempted':>11}{'Cold':>7}{'Wrong':>7}{'Hint':>7}{'Skip':>7}"]
    for r in rows:
        lines.append(f"{r['topic']:<{width}}{r['total']:>7}{r['attempted'] or 0:>11}{r['solved_cold'] or 0:>7}"
                      f"{r['wrong'] or 0:>7}{r['needed_hint'] or 0:>7}{r['skipped'] or 0:>7}")
    show_lines(screen, "Progress stats", lines)


def _curses_main(stdscr):
    conn = db.connect()
    screen = Screen(stdscr)
    screen.set_header("practice.py -- ISRO exam practice")
    menu = ["Practice (next batch of 3)", "Practice by topic", "Stats", "Quit"]
    try:
        while True:
            try:
                choice = pick_one(screen, "Main menu", menu)
            except Back:
                continue
            if choice == 0:
                run_batch(screen, conn)
            elif choice == 1:
                topics = [r["topic"] for r in conn.execute(
                    "SELECT DISTINCT topic FROM questions ORDER BY topic").fetchall()]
                try:
                    t = pick_one(screen, "Pick a topic", topics)
                except Back:
                    continue
                run_batch(screen, conn, topic=topics[t])
            elif choice == 2:
                run_stats(screen, conn)
            elif choice == 3:
                return
    except Quit:
        return
    finally:
        conn.close()
