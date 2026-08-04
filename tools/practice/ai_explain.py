"""Shells out to the `claude` CLI in one-shot mode (`claude -p`) for
interactive, per-question Q&A during practice -- when hints alone aren't
enough, you can ask a free-form question at any point (cold, or after
hint 1/2/3, or with the link shown). One-shot, not an interactive session:
a single subprocess call with no tool use, billed the same as any other
Claude Code usage under the logged-in account.

Every turn is logged by db.py into ai_chat_log, and each new ask passes the
prior logged thread back in as context so answers build on what was
already discussed for that question instead of repeating it.
"""
import json
import subprocess

MODEL = "haiku"
TIMEOUT_S = 60
DEFAULT_QUERY = "Explain the reasoning/method needed to solve this."


class ExplainError(Exception):
    pass


def _question_context(row):
    lines = [
        f"Question ({row['topic']}" + (f" - {row['subtopic']})" if row["subtopic"] else ")"),
        row["question_text"],
    ]
    for letter in "abcd":
        opt = row[f"option_{letter}"]
        if opt:
            lines.append(f"({letter}) {opt}")
    if row["correct_answer"]:
        correct_opt = row[f"option_{row['correct_answer']}"]
        lines.append(f"Correct answer: ({row['correct_answer']}) {correct_opt}")
    return "\n".join(lines)


def _build_prompt(row, revealed_hints, thread, user_query):
    parts = [_question_context(row)]
    if revealed_hints:
        parts.append("Hints shown so far: " + " | ".join(h["hint_text"] for h in revealed_hints))
    if thread:
        parts.append("Conversation so far on this question:")
        for t in thread:
            speaker = "Learner" if t["role"] == "user" else "You"
            parts.append(f"{speaker}: {t['message']}")
    parts.append(f"Learner: {user_query or DEFAULT_QUERY}")
    parts.append("Reply in 2-5 sentences, plain text only -- no markdown, no URLs or links.")
    return "\n".join(parts)


def ask(row, revealed_hints, thread, user_query):
    """thread: prior ai_chat_log rows for this question, oldest first.
    Returns the reply text, or raises ExplainError."""
    prompt = _build_prompt(row, revealed_hints, thread, user_query)
    try:
        proc = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "json", "--model", MODEL],
            capture_output=True, text=True, timeout=TIMEOUT_S,
        )
    except FileNotFoundError:
        raise ExplainError("`claude` CLI not found on PATH.")
    except subprocess.TimeoutExpired:
        raise ExplainError("timed out waiting for a response.")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise ExplainError((proc.stderr or proc.stdout or "empty output").strip()[:200])

    if data.get("is_error"):
        raise ExplainError(data.get("result") or "claude returned an error.")
    result = data.get("result")
    if not result:
        raise ExplainError("empty response.")
    return result.strip()
