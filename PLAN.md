# Job Radar: gap-closer #1 plan

**One line:** a daily Python pipeline that collects open roles from target companies' public job-board APIs, scores each one against my profile (skills, target roles, level, location, goals), and surfaces the best-fit opportunities every morning, while building a historical dataset of the hiring market.

**Why it exists:**
1. **Find the right opportunities, early.** Good-fit roles were closing before I saw them. Job boards rank by keywords and recency; Job Radar ranks by fit with a specific, well-defined profile: what I'm strong at, what I'm learning, the roles I'm targeting and where I can work.
2. **Close my skill gaps by building it.** It's a gap-closer project: real API extraction, data modeling, cloud warehousing, automation, testing and monitoring. I write the code myself, learning as I go, with an AI assistant as pair programmer.
3. **Learn from the market.** Daily snapshots become a dataset nobody else has: which skills are in demand, which companies are hiring, and how long roles stay open.

---

## Architecture (v1)

```
companies.csv ──► extract (3 ATS adapters) ──► normalize + classify ──► validate
                                                                         │
     Looker Studio ◄── BigQuery views ◄── BigQuery: snapshots (append) ◄─┘
                              │
                              └──► daily email digest (new matches)

GitHub Actions cron (daily) runs it all · logging to file + Actions log · INCIDENTS.md
```

## Sources (verified Nov 3: all public, no key needed)

| ATS | Endpoint | Notes |
|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs` | `{"jobs": [...]}`; title, location.name, updated_at, first_published, absolute_url |
| Lever | `https://api.lever.co/v0/postings/{slug}?mode=json` | plain list; `text`, `categories.location/commitment`, `createdAt` in **ms epoch**, `workplaceType` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{slug}` | `{"jobs": [...]}`; `isRemote`, `workplaceType`, `employmentType`, `publishedAt` |

Three schemas, three date formats, so normalization is a real problem (good).

**v2:** Workday adapter (used by many big tech companies), then custom careers sites (Google, Microsoft, Amazon, Meta, Apple) if feasible.

## Company list: `companies.csv`

`company, ats, slug, segment, region, tier`
- Top 15 + watchlist (Monday "Target Companies")
- AI labs / AI-native companies, martech SaaS, data-driven agencies
- **Big tech internships and early-career programs** (v1: those on Greenhouse/Lever/Ashby; rest in v2)
- Target: about 40–60 companies in v1. Verify each slug by opening the endpoint in a browser.

## Data model (BigQuery)

- `raw.snapshots`: one row per posting per day (`snapshot_date, company, ats, job_id, title, location, remote_flag, employment_type, url, published_at, ...`). **Append-only load jobs**, so the design works on the free BigQuery sandbox (no MERGE/UPDATE needed).
- `analytics.postings` (view): one row per posting, with `first_seen`, `last_seen`, `is_open`, `days_open`.
- `analytics.new_today` (view): postings first seen today that match my filters.
- `ops.runs`: one row per run (start, end, companies ok/failed, rows loaded, errors).

## Classification + fit scoring (rules, v1)

My profile lives in `profile.yaml` (skills with levels, target role families, seniority, location/work-rights, must-haves and deal-breakers), so the scoring logic never hardcodes who I am and can be reused for any profile.

- **role_family:** data/analytics · AI ops / data quality / AI training · solutions / implementation / customer success analyst · marketing / growth · other
- **level:** intern / graduate / apprentice / residency / fellowship → `early_career`; junior · mid · senior (from title keywords)
- **location fit:** remote-worldwide · remote-LatAm/Mexico · Australia · other
- **fit_score (0–100):** role-family match + level match + location/work-rights fit + skill overlap with the posting (keywords v1, description parsing v2) − deal-breakers (on-site only, senior-only, residency required)
- **gap_skills:** skills the posting asks for that I don't have yet → feeds my learning plan
- **Digest = new postings with fit_score above threshold, ranked**

## Production checklist (this is the actual point)

- [ ] Retries with exponential backoff and timeouts on every request
- [ ] One company failing never kills the run (isolate, log, continue)
- [ ] Structured logging (`logging`, INFO/WARNING/ERROR) + run summary row in `ops.runs`
- [ ] Validation before load: required fields, dedupe on (company, job_id, date), row-count sanity check vs yesterday
- [ ] Idempotent: re-running the same day doesn't duplicate rows
- [ ] Config in `companies.csv` + `config.yaml`; secrets only in GitHub Secrets / `.env`
- [ ] Unit tests for the 3 parsers (pytest, with saved sample JSON)
- [ ] GitHub Actions daily cron + failure notification
- [ ] `INCIDENTS.md`: every real break documented (symptom → cause → fix → prevention)

## Milestones

| # | Milestone | Done when |
|---|---|---|
| 0 | Setup | GitHub repo, venv, GCP project + BigQuery sandbox, service account key works |
| 1 | Extract | 3 adapters return raw JSON for 5 test companies, with retries + logging |
| 2 | Normalize + classify | One clean DataFrame, same columns for all ATS; tests pass |
| 3 | Load | Snapshot rows land in BigQuery; views return first_seen / is_open |
| 4 | Automate | GitHub Actions runs daily on its own |
| 5 | Use it | Ranked email digest of best-fit new roles + Looker Studio dashboard (fit, gaps, market trends) |
| 6 | Ship | README, architecture diagram, INCIDENTS.md, LinkedIn post |

**v1 is done when:** it ran 7 days in a row unattended, covers 40+ companies, the digest arrives every morning, the dashboard is public, and at least 3 incidents are documented.

**After 30 days:** analysis posts from the data, e.g. "Which skills do analyst roles actually ask for?" and "How long do they stay open?"

## How we build it

Steph writes the code; Claude scaffolds, explains, gives hints and reviews: it points at the problem and doesn't hand over the answer. The skill is the point.

Job Radar is one part of a daily training system that runs alongside the build:

- **Daily 5:** five timed reasoning and CS questions every morning (number series, rates, logic puzzles, OOP, SQL), with misses reviewed.
- **ANSI SQL practice:** standard-SQL drills, one question at a time (execution order, NULLs, joins, window functions, CTEs).
- **Technical-assessment training:** timed, exercise-style practice that mirrors tech-company hiring tests (problem solving, cognitive speed, OOP, data structures, Big-O).
- **Python training:** small exercises tied to this project (APIs and JSON, data structures, classes, testing) that become real code here.
- **Interview practice:** timed answers from a personal answer bank, with feedback.

Each milestone of this repo is where that practice turns into shipped, working code.
