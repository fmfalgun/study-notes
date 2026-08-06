# Cybersecurity Dev Track — Someday Checklist

Things worth exploring later, deliberately not now. Each entry logs *when/where/how* the idea
came up so it stays traceable back to its origin instead of floating as an orphaned bullet.

## Format

```
- [ ] <topic>
  - **Origin:** date, which file/exercise/conversation it came from, what triggered it
  - **What to explore:** the actual question/task for future-us
  - **Key terms:** exact vocabulary to search for (so future search doesn't start from zero)
```

## Entries

- [ ] Opportunistic automated scraping of secrets/keys pushed to public git repos
  - **Origin:** 2026-08-05, `00-prerequisite-foundations/` session — came up while justifying why
    `generated-keys/` is gitignored (cybersecurity-based justification for never pushing real key
    material, even study keys).
  - **What to explore:** how fast and how automated real-world credential-scraping bots actually
    are against public GitHub pushes; what defensive tooling exists to catch this before/at push
    time (pre-commit hooks vs. platform-level scanning); how "canary"/honeytoken keys are used to
    empirically measure attacker response time.
  - **Key terms:**
    - **Secrets sprawl** — the umbrella industry term (coined/tracked by GitGuardian, who publish
      an annual "State of Secrets Sprawl" report) for secrets ending up scattered across repos,
      logs, configs, container images, etc.
    - **Secret scanning** — the actual named activity/technique, used by both sides: GitHub's own
      built-in feature is literally called "Secret Scanning" (+ "Push Protection" to block a push
      before it lands); the same name covers attacker-side scanning tools like **TruffleHog**,
      **Gitleaks**, and **Gitrob**.
    - **Canary tokens / honeytokens** — deliberately-planted fake credentials used defensively to
      measure how fast leaked secrets get discovered and abused in the wild.
    - Primary research citation: Meli, McNiece, Reaves, **"How Bad Can It Git? Characterizing
      Secret Leakage in Public GitHub Repositories"** (NDSS 2019) — six-month live scan of public
      GitHub commits; found a median of ~1,793 unique secrets leaked per day, with a **median
      time-to-discovery of just 20 seconds** (range: half a second to just over 4 minutes).
