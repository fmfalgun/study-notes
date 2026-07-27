"""Shells out to the `claude` CLI in one-shot mode (`claude -p`) to generate
a short explanation for a practice question, for when the stored hints
aren't enough. One-shot, not an interactive session -- a single subprocess
call with no tool use, billed the same as any other Claude Code usage under
the logged-in account. Results are cached by db.py's ai_explanations table
so a question is only ever sent to the model once.
"""
import json
import subprocess

MODEL = "haiku"
TIMEOUT_S = 60


class ExplainError(Exception):
    pass


def _build_prompt(row, hints):
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
    if hints:
        lines.append("Hints already shown: " + " | ".join(h["hint_text"] for h in hints))
    lines.append(
        "In 3-5 sentences, explain the reasoning/method needed to solve this, "
        "building on the hints already shown rather than repeating them. "
        "Plain text only -- no markdown, no URLs or links."
    )
    return "\n".join(lines)


def generate(row, hints):
    """Returns the explanation text, or raises ExplainError."""
    prompt = _build_prompt(row, hints)
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
