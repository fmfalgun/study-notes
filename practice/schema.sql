-- Practice-problem tracker for ISRO exam prep.
-- One row per real question from the previous attempt paper (Set C, isro-prev-attempt-1/).

CREATE TABLE IF NOT EXISTS questions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_q_num     INTEGER,                 -- original Q number (1-95) in isro-prev-attempt-1, NULL if added later
    part            TEXT CHECK(part IN ('A','B')),
    topic           TEXT NOT NULL,           -- e.g. 'Operating System'
    subtopic        TEXT,                    -- e.g. "Deadlock - Banker's Algorithm"
    tier            TEXT,                    -- '1' / '2' / '3' / 'shadow' per exam-priority-report.md
    difficulty      TEXT CHECK(difficulty IN ('Easy','Medium','Complex')),
    question_text   TEXT NOT NULL,
    option_a        TEXT,
    option_b        TEXT,
    option_c        TEXT,
    option_d        TEXT,
    correct_answer  TEXT CHECK(correct_answer IN ('a','b','c','d')),
    answer_status   TEXT CHECK(answer_status IN ('verified','unverified')) DEFAULT 'unverified',
    answer_notes    TEXT,                    -- brief reasoning / ambiguity flag
    source_image    TEXT,                    -- originating photo filename, for traceability
    added_at        TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attempts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL REFERENCES questions(id),
    attempted_at    TEXT DEFAULT CURRENT_TIMESTAMP,
    selected_answer TEXT CHECK(selected_answer IN ('a','b','c','d')),
    outcome         TEXT NOT NULL CHECK(outcome IN ('solved_cold','needed_hint','wrong','skipped')),
    notes           TEXT
);

CREATE INDEX IF NOT EXISTS idx_attempts_question ON attempts(question_id);

-- Up to 3 progressively-revealing hints per question. A separate table
-- (not hint_1/hint_2/hint_3 columns on questions) since a hint is a
-- repeating group keyed by (question_id, hint_order), not an attribute
-- of the question row itself.
CREATE TABLE IF NOT EXISTS hints (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL REFERENCES questions(id),
    hint_order      INTEGER NOT NULL CHECK(hint_order IN (1,2,3)),
    hint_text       TEXT NOT NULL,
    UNIQUE(question_id, hint_order)
);

CREATE INDEX IF NOT EXISTS idx_hints_question ON hints(question_id);

-- One reference link per topic (not per question) -- the "fundamentals"
-- link depends on the topic, not on any individual question, so keying
-- it by question_id would just repeat the same URL across every
-- question sharing a topic.
CREATE TABLE IF NOT EXISTS topic_links (
    topic           TEXT PRIMARY KEY,
    link            TEXT NOT NULL
);

-- Single persisted row (id=1) holding the in-progress batch's remaining
-- question ids, so relaunching the TUI resumes the exact question you were
-- on -- a new batch is only drawn once the current one is fully answered
-- or skipped, not on every login.
CREATE TABLE IF NOT EXISTS session_state (
    id              INTEGER PRIMARY KEY CHECK(id = 1),
    topic           TEXT,
    batch_ids       TEXT NOT NULL
);

-- Cached AI-generated explanation per question, produced on demand by
-- shelling out to the `claude` CLI (see ai_explain.py) the first time a
-- learner asks for one. Cached so every later encounter with the same
-- question is a free DB read instead of a re-query of the model.
CREATE TABLE IF NOT EXISTS ai_explanations (
    question_id     INTEGER PRIMARY KEY REFERENCES questions(id),
    explanation     TEXT NOT NULL,
    model           TEXT,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);
