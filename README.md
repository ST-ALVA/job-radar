# Job Radar

**Finds the roles that fit your profile, ranks them, flags your gaps, and gets you there before the crowd.**

Job boards rank by keywords and recency. Job Radar ranks by **fit**: every morning it collects new openings from target companies, scores each one against a candidate profile (skills, target roles, level, location and work rights, deal-breakers), and surfaces the best matches first, along with the skills each role asks for that the candidate doesn't have yet.

It also builds a daily historical dataset of the hiring market: which skills are in demand, which companies are hiring, and how long roles stay open.

## How it works

```
companies.csv ─► extract (one adapter per ATS) ─► parse to a standard schema ─► score fit vs profile.yaml
                                                                                        │
     dashboard ◄── BigQuery views ◄── BigQuery daily snapshots (append-only) ◄──────────┘
                         │
                         └──► morning digest: new roles, ranked by fit, with gap skills
```

- **Extract:** one small adapter per applicant tracking system (ATS), each pulling from that platform's public job-board API.
- **Parse:** each adapter converts its platform's raw format into the same standard fields (`job_id`, `title`, `location`, `url`, `published_at`), so every source lands in one table.
- **Fit scoring:** the candidate's profile lives in `profile.yaml`, so the logic never hardcodes who the candidate is and works for any profile.
- **Load and track:** daily snapshots in BigQuery; views compute first seen, last seen, days open and what's new today.

## Built so far

- [x] Project skeleton, virtual environment, pinned dependencies
- [x] First ATS adapter: fetch jobs for any company slug
- [x] Production habits: request timeouts, structured logging, retries with exponential backoff, no retries on permanent errors (4xx)
- [x] Parser to the standard schema
- [x] Unit tests (pytest) against a saved sample, so tests never hit the live API

## Roadmap

| Milestone | What | Status |
|---|---|---|
| 1 | Extract: adapters for the main ATS platforms, retries, logging | in progress |
| 2 | Normalize and classify: one clean table across all sources, role family, level, location fit | next |
| 3 | Load: append-only daily snapshots in BigQuery + views | |
| 4 | Automate: GitHub Actions daily run, failure alerts, incident log | |
| 5 | Use it: ranked morning digest + public dashboard (fit, gaps, time-to-close, market trends) | |
| 6 | **v2 fit engine:** an LLM (Claude) reads each posting against the full profile and CV and returns a fit score, the reasons and the gaps | |

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.extract.greenhouse   # fetch one company's jobs (logs to the terminal)
pytest -v                          # run the tests
```

Python 3.12+.

## How it's built

I'm a data analyst with a background in branding and design, and this is my first production-style pipeline. I write the code myself, learning as I go, with an AI assistant as pair programmer: it explains and reviews; it doesn't hand me the answers. The full plan, architecture and production checklist are in [PLAN.md](PLAN.md).
