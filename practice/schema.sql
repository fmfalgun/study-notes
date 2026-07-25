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
