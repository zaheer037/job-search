# Search Queries for Job Scraper

<!-- SETUP: Customize these queries based on your skills, target roles, and location -->

## Installed portal CLIs (primary for `/scrape`)

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first. Shipped country-agnostic CLIs include `linkedin-search` and `freehire-search`; Danish demos and any skill you add with `/add-portal` are included the same way. You do **not** need a matching `site:` line below for those CLIs to run.

The `site:` query templates in this file are the **WebSearch fallback** — for portals without a CLI, company career pages, or when a CLI fails.

**Language scope:** write every query category in every language listed in your AGENTS.md Languages table (typically 1-2, sometimes more). A posting requiring a language you have *not* declared, as a job condition, is excluded before scoring; a posting requiring a *higher level* than you declared in a language you *do* work in is flagged for your own judgment, not excluded — see `04-job-evaluation.md`'s Language Gate, the single source of truth for this rule. Translate each category's keywords rather than machine-translating word-for-word (e.g. "Frontend Developer" -> "Desarrollador Frontend", not a literal word-for-word translation) if you work in more than one language.

## Search Sites

Primary:
- **linkedin.com/jobs** - LinkedIn job listings (filter: India, Hyderabad, Bengaluru, Remote); covered by `linkedin-search` CLI
- **freehire.me** - Aggregated developer/data roles; covered by `freehire-search` CLI
- **naukri.com** - Leading job board for tech and data engineering in India
- **instahyre.com / wellfound.com** - Tech startup and scale-up engineering roles

Secondary (company career pages via Google):
- Direct Google searches with `site:` filters for known target companies and ATS platforms (Greenhouse, Lever, Ashby, Workday)

## Query Categories

Queries are organized by functional domain and role priorities:

### Priority 1: Data Engineering & Pipeline Engineering

Primary career focus matching core competencies in Python, SQL, Celery, PostgreSQL, DuckDB, AWS.

Lead with entry-level wording (see the Experience Filter below): "junior", "associate", "entry level", "fresher", "trainee", "Data Engineer I". On `freehire-search`, add `--seniority junior`.

```
site:linkedin.com/jobs "Junior Data Engineer" OR "Associate Data Engineer" OR "Data Engineer I" India
site:linkedin.com/jobs "Data Engineer" "fresher" OR "entry level" OR "0-2 years" India
site:linkedin.com/jobs "Data Engineer" "Python" "SQL" India
site:linkedin.com/jobs "Data Engineer" Hyderabad OR Bangalore OR Bengaluru OR Remote
site:naukri.com "Data Engineer" "Python" "PostgreSQL" "AWS"
site:naukri.com "Associate Data Engineer" OR "Junior Data Engineer"
```

### Priority 2: Python Backend & Distributed Task Engineering

Asynchronous backend and data infrastructure roles matching FastAPI, Celery, Redis, and cloud services.

```
site:linkedin.com/jobs "Python Backend Engineer" "FastAPI" OR "Celery" India
site:linkedin.com/jobs "Backend Developer" "Python" "PostgreSQL" Remote
site:naukri.com "Python Developer" "FastAPI" "PostgreSQL"
```

### Priority 3: Analytics Engineering & ETL/ELT Systems

Analytics engineering, database transformations, and analytical query modeling (DuckDB, SQL, Parquet).

```
site:linkedin.com/jobs "Analytics Engineer" "SQL" "Python" India
site:linkedin.com/jobs "ETL Developer" OR "Pipeline Engineer" India
site:naukri.com "Analytics Engineer" "SQL" "PostgreSQL"
```

### Priority 4: Broader Tech / Startup Data Engineering

Broader searches across high-growth startups and tech platforms.

```
site:wellfound.com "Data Engineer" Python SQL Remote
site:instahyre.com "Data Engineer" "Python" "PostgreSQL"
```

## Location Filter

When evaluating results, verify the job location matches the candidate's preferences:
- **Remote**: 100% Remote / Work from Home (India or Global) - IDEAL (PASS)
- **Hyderabad, Telangana**: High preference (PASS)
- **Bengaluru / Bangalore, Karnataka**: High preference (PASS)
- **Andhra Pradesh / Guntur / Vijayawada**: Local / Hybrid (PASS)
- **Other Major Indian Tech Hubs (Chennai, Pune, Gurgaon/Noida)**: ACCEPTABLE with hybrid/relocation support (PASS)
- **Strict On-site in other locations with no relocation support**: FAIL

## Experience Filter

The candidate has **under 1 year of full-time experience** (Junior Data Engineer since Jan 2026) plus two summer 2025 internships. Read each posting's stated minimum experience before assigning fit - skill match alone never makes a role High fit:
- **Fresher / 0-1 years / 0-2 years / entry level / graduate or trainee / "1+ years including internships"**: realistic - score on skills as normal
- **1-2 or 1-3 years**: stretch - keep, flag the gap
- **2+ years minimum**: Low fit regardless of skill match
- **3+ years minimum, or Senior / Lead / Staff / II / III / Specialist titles**: skip
- **No years stated**: judge from title and responsibilities ("expert-level", "proven expertise", "own the architecture" read as mid-level) and flag "years not stated"

Watch for postings that rate individual skills "entry level (1-3 years)" but state a higher overall minimum elsewhere (e.g. "Exp - 5+ years"): the overall minimum wins.

## Language Filter

Your working languages and levels are in AGENTS.md's Languages table. When filtering scraped results, apply `04-job-evaluation.md`'s Language Gate: a posting requiring a language you haven't declared at all is excluded; a posting requiring a higher level than you declared in a language you do work in is not excluded, flag it clearly instead (see `job-scraper/SKILL.md`'s Step 3 "Quick Fit Assessment" for how the flag surfaces in `/scrape` output). Postings simply *written* in a language you don't work in, that don't require it on the job, are fine.

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- "/scrape [focus_area]" -> relevant category queries + custom focus-specific queries
