<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the courier bird" width="200">
</p>

# AI Job Search

*The job search that runs on your machine.*

<p align="center">
  <a href="https://trendshift.io/repositories/43622?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-43622" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/43622/daily" alt="MadsLorentzen%2Fai-job-search | Trendshift" width="250" height="55"/></a>
</p>

[![CI](https://github.com/zaheer037/job-search/actions/workflows/ci.yml/badge.svg)](https://github.com/zaheer037/job-search/actions/workflows/ci.yml)

An AI-powered job application framework that runs on **any** agentic coding tool — [Google Antigravity](https://antigravity.google), [Claude Code](https://claude.com/claude-code), Codex, Gemini CLI, Cursor. Fork it, fill in your profile, and let your agent evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews.

Workflows live in the portable [Agent Skills](https://agentskills.dev) format under [`.agents/skills/`](.agents/skills/), with root instructions in [`AGENTS.md`](AGENTS.md). Runtimes that need their own paths get generated projections — see [Runtimes](#runtimes).

> Note: This is an independent open-source project and is not affiliated with, endorsed by, sponsored by, or maintained by Anthropic. Anthropic and Claude Code are referenced only to describe the toolchain this workflow uses.
>
> This project has **no affiliated cryptocurrency, token, or paid sponsorship program**. Anything claiming otherwise is unauthorized and should be treated as a scam. The only ways to support the project are the Ko-fi link below and contributing on GitHub.

## Does it actually work?

I'm a geophysicist by training. When my position was cut in late 2025, I built this framework to run my own job search - the same `/scrape`, `/apply`, and `/interview` workflow in this repo, used weekly, on my own career. I was upfront about it with every employer I spoke to, and instead of counting against me, it usually sparked a genuine technical conversation.

Sixty-nine tailored applications, twenty first interviews, and one signed contract later, I started as an AI engineer in June 2026. People kept asking whether this actually works. It got me hired. Now it's yours.

*The longer version, including the full application funnel, is on [LinkedIn](https://www.linkedin.com/in/mads-lorentzen/).*

<p align="center">
  <i>Did this save you a Sunday of cover-letter writing? Consider a coffee.<br>
  Did it land you the job? Maybe two.</i> ☕
</p>

<p align="center">
  <a href="https://ko-fi.com/madslorentzen">
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=6" alt="Buy me a coffee at ko-fi.com" height="40">
  </a>
</p>

## What this is

A structured workflow that turns any agentic coding tool into a full-stack job application assistant. The core workflow (self-profiling, fit evaluation, and the drafter-reviewer application pipeline) is **language- and country-agnostic**. The job portal search skills are built for the Danish market (Jobindex, Jobnet, Akademikernes Jobbank, etc.), but the pattern is designed to be swapped for your local job boards.

```
/setup          /scrape              /apply <url>
  |                |                     |
  v                v                     v
Fill in        Search job           Evaluate fit
your profile   portals              Score & recommend
  |                |                     |
  v                v                     v
Profile        Present matches      Draft CV + Cover Letter
files ready    with fit ratings     (LaTeX, tailored)
                   |                     |
                   v                     v
               Pick a match         Reviewer agent critiques
               -> /apply            -> Revise -> Final output
```

The framework encodes career guidance best practices, including structured evaluation criteria, forward-looking cover letter framing, and optional salary benchmarking.

## Prerequisites

- **An agentic coding tool.** Any of these work; see [Runtimes](#runtimes) for what each needs:
  [Google Antigravity](https://antigravity.google) (free tier available),
  [Claude Code](https://claude.com/claude-code) (needs a Claude Pro/Max/Team subscription or
  Anthropic API credits — no free tier), Codex, Gemini CLI, Cursor, Copilot, Jules, Aider.
- Python 3.10+
- [Bun](https://bun.sh) (for job search CLI tools)
- LaTeX distribution with `lualatex` and `xelatex`: [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), [TinyTeX](https://yihui.org/tinytex/), or [MiKTeX](https://miktex.org/). The CV compiles with `lualatex` (pdflatex often fails on modern MiKTeX installs with `fontawesome5` font-expansion errors); the cover letter compiles with `xelatex` because `cover.cls` requires `fontspec`. If using a minimal TeX install such as TinyTeX or BasicTeX, install the extra packages listed in [SETUP.md](SETUP.md#minimal-tex-install-tinytexbasictex).
- Optional: `pip install pypdf` for `/apply`'s ATS parseability check (BSD; no Poppler required). Poppler `pdftotext` remains a fallback (macOS: `brew install poppler`, Debian/Ubuntu: `apt install poppler-utils`, Windows: `choco install poppler`). If both are missing, the check degrades to a visual keyword review.

## Runtimes

Workflows live once, under [`.agents/skills/`](.agents/skills/), in the portable Agent Skills
format. Root instructions live once, in [`AGENTS.md`](AGENTS.md). Runtimes that insist on
their own paths get a **projection** — a symlink, or a stub that imports the canonical file —
so there is no second copy of any rule and nothing to keep in sync by hand.

```bash
python3 tools/agent_sync.py            # create/repair the projections (run once after cloning)
python3 tools/agent_sync.py --check    # verify they are intact
python3 tools/agent_sync.py --copy     # real files instead of symlinks (Windows without dev mode)
```

| Runtime | Reads | Skills | Extra setup |
|---|---|---|---|
| **Google Antigravity** | `AGENTS.md`, `.agents/rules/` | `.agents/skills/` natively | none — it is the native layout |
| **Claude Code** | `CLAUDE.md` → imports `AGENTS.md` | `.claude/skills` symlink | `agent_sync.py` (or `--copy`) |
| **Gemini CLI** | `GEMINI.md` → `AGENTS.md` | reads skill files on request | `agent_sync.py` |
| **Codex / Cursor / Copilot / Jules / Aider** | `AGENTS.md` | reads skill files on request | none |

Every workflow is invoked the same way everywhere: `/<skill-directory-name>` where the runtime
supports slash commands (`/setup`, `/scrape`, `/rank`, `/apply`, …), and otherwise by asking
in plain language — "run the setup skill", "rank my scraped jobs". `tools/lint_skills.py`
pins each skill's frontmatter `name` to its directory name, so the same workflow answers to
the same `/name` no matter which runtime reads the workspace.

**Missing a capability?** Skill bodies name one runtime's tools (`WebFetch`, `Glob`, the Agent
tool). The capability table in [`AGENTS.md`](AGENTS.md#capability-map) maps them to yours, and
the rule when something is genuinely absent is **degrade, then disclose**: do the sequential or
shell equivalent and say which step ran degraded. A posting that could not be fetched is never
scored from its title.

**Permissions.** `.claude/settings.json` pre-approves the portal CLIs and helper scripts for
Claude Code. Other runtimes prompt on first use, or accept an allowlist of their own — mirror
[`.agents/rules/allowed-commands.md`](.agents/rules/allowed-commands.md) into it.

## Quick start

> 🎥 **Prefer to see it in action first?** [The Next New Thing did a hands-on walkthrough](https://www.youtube.com/watch?v=HoVxjMNFYv4) of how the workflow is actually used, from setup to a finished application (recorded August 2026 - commands may have evolved since).

### 1. Fork and clone

**To use it for your own job search** (what almost everyone wants) — clone, and keep
your copy **private**:

```bash
git clone https://github.com/zaheer037/job-search.git
cd job-search
```

**To contribute changes back** — fork first:

```bash
gh repo fork zaheer037/job-search --clone
cd job-search
```

> [!IMPORTANT]
> **A fork of this repo is always public** — GitHub does not allow private forks of
> public repositories — and `/setup` (step 3) writes your personal data (name,
> contact details, employment history, salary expectations) into **tracked** files.
> If this copy is for your own job search rather than for contributing changes back,
> use a **private repository** with this repo as `upstream` instead — the two-minute
> recipe is in [SETUP.md section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork),
> and every update workflow works identically. Fork only to contribute.

### 2. Install

```bash
./install.sh
```

Windows: `.\install.ps1`. Anywhere: `python3 tools/install.py`.

That is the whole install. There is no per-agent step — it detects the agents you
have and configures all of them in one pass:

| | |
|---|---|
| **Prerequisites** | checks Python, bun, LaTeX, `pdftotext`/`pypdf`, and tells you what each missing one costs — nothing silently degrades |
| **Runtimes** | reports which agents it can see (Antigravity, Claude Code, Codex, Gemini CLI, Cursor, Copilot, Aider) |
| **Projections** | writes `CLAUDE.md`, `GEMINI.md` and the `.claude/skills` symlink from the canonical `.agents/` tree |
| **Portal CLIs** | runs `bun install` for all six job-board search tools |
| **Verify** | lints the 21 skills and fails loudly rather than half-installing |

Nothing is written outside the repo directory. Re-run it any time — it is idempotent
— and `./install.sh --check` verifies an existing install without changing anything.

Only Python 3.10+ is strictly required. Missing bun just disables `/scrape`; missing
LaTeX means you get `.tex` files but no compiled `.pdf`. Install either later and
re-run `./install.sh` to pick it up.

### 3. Set up your profile

Open the repo in your agent and run `/setup` — Antigravity and Claude Code expose it
as a slash command; elsewhere just say "run the setup skill":

```
/setup
```

`/setup` offers three paths: read your `documents/` folder if you have one populated (CV PDF, LinkedIn export, diplomas, reference letters, past applications), import a single CV pasted in chat, or walk through an interview. It auto-detects what you have and asks. Documents-folder mode is idempotent and safe to re-run as you add more material; see `documents/README.md` for the layout.

### 4. Search for jobs

```bash
/scrape
```

This searches multiple job portals for positions matching your profile, deduplicates results, and presents them sorted by fit. Pick a match to run `/apply` on it directly — or, when a scrape returns more jobs than you want to eyeball, run `/rank` to batch-score them all against the fit framework and get a ranked shortlist first.

### 5. Apply to a job

```bash
/apply https://jobindex.dk/job/1234567
```

If the URL can't be fetched (some job portals block automated access), you can paste the job description directly instead:

```bash
/apply <paste the full job description here>
```

This runs the full workflow: evaluate fit, draft CV + cover letter, review with a second agent, revise, and present the final output.

Postings are treated as untrusted input (the workflow follows no instructions embedded in them and fetches no links from their body), but agentic defenses are instruction-level, not a sandbox - on an unfamiliar job board, skim what was fetched and written before you hit send. Details in [SECURITY.md](SECURITY.md).

## Your market

The workflow — fit scoring, CV tailoring, cover letters, interview prep, tracking — is
country- and language-agnostic. Only the **job boards** are market-specific, and `/setup`
asks which ones fit your market before enabling anything.

| Portal | Coverage | Ships as |
|---|---|---|
| `linkedin-search` | **any country**; you pass `--location "Bengaluru, Karnataka, India"`, `"Berlin, Germany"`, `"Remote"` | enabled |
| `freehire-search` | **many markets**, tech/software/data roles; `--region apac\|eu\|us\|latam\|cis`, `--country IN,DE,GB` | enabled |
| `jobindex`, `jobnet`, `jobbank`, `jobdanmark` | Denmark | **disabled** — worked examples of the portal pattern; `/setup` enables them only if your market is Denmark |

So a new user anywhere starts with two working portals, not zero.

**For a board that isn't shipped** — Naukri, Instahyre, Indeed, Seek, StepStone — run
[`/add-portal`](#other-commands). It investigates the board, scaffolds a CLI with the same
contract as the shipped ones, and test-runs a live query before registering it. `/scrape`
auto-discovers whatever is installed; nothing to wire up. This is usually the highest-value
thing to do right after `/setup`.

**Language.** CVs default to English; `/setup` asks if your market expects otherwise. Cover
letters always match the posting's language automatically. The Language Gate in
`04-job-evaluation.md` hard-rejects a posting requiring a language you haven't declared, and
flags — rather than drops — one asking for a higher level than you claim.

**Salary benchmarking is bring-your-own-data** in every market, Denmark included.
`salary_lookup.py` reads a `salary_data.json` you build from whatever source you trust —
union statistics, a Glassdoor or levels.fyi export, numbers you collected yourself. See
[tools/README_SALARY_TOOL.md](tools/README_SALARY_TOOL.md).

## Other commands

`/setup`, `/scrape`, and `/apply` form the core workflow. At a glance:

| When | Command | What it does |
|---|---|---|
| **Once, first** | `/setup` | Builds your profile. Nothing else works until this has run. |
| Once, optional | `/expand` | Mines GitHub, portfolio, course syllabi for skills your CV doesn't spell out |
| Once, per market | `/add-portal` | Adds a job board the repo doesn't ship |
| Once, optional | `/add-template` | Registers your own CV/cover-letter design |
| **Every cycle** | `/scrape` → `/rank` → `/apply <url>` | Find → triage cheaply → apply properly |
| After applying | `/outcome` | Log interviews, offers, rejections, silence; draft follow-ups |
| Before an interview | `/interview` | Stage-specific prep pack + optional mock interview |
| Whenever | `/gmail-sync` | Detect status changes from your inbox |
| Periodically | `/upskill` | Skill gaps across tracked jobs + a learning plan |
| Periodically | `/html-report`, `/notion-sync` | Offline dashboard; live Notion view |
| Starting over | `/reset` | Wipes profile data. Destructive — never auto-triggers |

Run `/rank` on every scrape: it scores from posting text alone, so it is cheap. Spend
`/apply` — which adds company research, drafting and PDF verification — only on what
survives it.

The `*-search` skills and `/job-application-assistant` are invoked by `/scrape` and
`/apply`; you don't call them directly.

Ten commands extend the core workflow once your profile is in place:

- **`/interview`** preps you for a scheduled interview on a tracked application. It builds a stage-specific prep pack from the application's archive (the exact posting, the CV and cover letter the interviewer actually read, feedback recorded from earlier rounds), researches the company and interviewers with a verify-before-use rule, maps likely questions to your STAR examples, and offers a mock interview following the roleplay protocol in `07-interview-prep.md`. Gaps get honest bridge answers, never invented experience.
- **`/outcome`** records what happened to an application - interview stages, offers, rejections, silence. It archives the submitted CV, cover letter, and posting text into `documents/applications/<company>_<role>/`, keeps `outcome.md` in the format `/setup` Path A parses, and updates the tracker. It also owns the stretch before there is an outcome to record: `/outcome followup` surfaces open applications that have gone quiet (default 10 days), drafts a short channel-appropriate follow-up in your writing style using only claims from the materials you already submitted (drafts only, never sends; at most twice per application), and offers a thank-you note in the same turn an interview stage is recorded. Once a few applications resolve, it points you back to `/setup` to calibrate the fit framework from what actually got interviews.
- **`/notion-sync`** publishes a one-way, read-only view of the pipeline into a Notion database via the official Notion MCP server (OAuth, no API keys) - one row per ranked job plus every tracked application, with a write-once briefing page per row. The repo files stay the system of record: nothing syncs back, and documents sync as filenames only. Complements `/html-report`: that is the deep offline dashboard you regenerate at your desk; this is the glanceable live view from anywhere Notion runs (desktop, web, phone).
- **`/gmail-sync`** reads your Gmail (via the Gmail connector) for status signals on your open applications - interview invites, assessment links, offers, rejections - and proposes them as a batch for you to approve before anything is written to the tracker or `outcome.md`, citing the source email on every proposed change. Offers stop short of proposing `hired`/`offer_declined` since that's your call; conflicting or unmatched signals get flagged for a manual `/outcome` pass instead of guessed.
- **`/rank`** bridges `/scrape` and `/apply`: it batch-scores all newly scraped postings against the fit framework (parallel agents fetch each posting and score the five evaluation dimensions) and returns a ranked shortlist with honest per-job strengths and gaps. Deal-breakers veto, deadlines get urgency flags, dead postings get marked expired. Pick a number and it hands off to the full `/apply` workflow.
- **`/expand`** enriches your profile by scanning public sources you've already linked in it (GitHub repos, portfolio site, Kaggle, Google Scholar) and looking up syllabi for named courses and certifications. Discovered competencies are added to your profile with a source tag. Useful right after `/setup` to surface skills that documents alone don't make explicit.
- **`/upskill`** analyzes the gap between your profile, your tracked job postings, and your ranked-but-untracked postings (`/rank`'s recorded gaps in `seen_jobs.json`) — or a single posting via `/upskill <URL>`. Produces a prioritized heatmap of skill gaps and a learning plan with web-searched study resources and time estimates. Useful for career planning between applications.
- **`/html-report`** generates a self-contained HTML dashboard from `job_search_tracker.csv` and the application archives — stat cards, status/sector/channel/funnel charts (inline SVG, no external dependencies), and a filterable applications table. Opens directly in a browser, fully offline. Re-run it any time after `/apply` or `/outcome` adds new entries.
- **`/add-template`** registers your own CV or cover letter template (LaTeX, Typst, or another toolchain) in place of the stock ones. It captures the template's instructions (source extension, compile command, fonts, style rules, page limit), runs a mandatory test compile, and wires the template into `/apply`. See [Custom templates](#custom-templates) below.
- **`/add-portal`** generates a job-portal search skill for a job board in your market. It investigates the portal (search URL pattern, result structure, access rules), scaffolds the CLI skill from the same structure as the shipped ones, and test-runs a live query before registering. See [Job search tools](#job-search-tools) below.

`/reset` is also available, see [Starting over](#starting-over) below.

## File structure

```
ai-job-search/
├── AGENTS.md                          # CANONICAL: candidate profile, workflow rules, runtime contract
├── .agents/
│   ├── rules/                         # Runtime-neutral rules (Antigravity auto-loads these)
│   │   ├── 00-workspace.md            # Where things live, degrade-then-disclose, non-negotiables
│   │   └── allowed-commands.md        # Canonical command allowlist to mirror into your runtime
│   └── skills/                        # CANONICAL: every workflow, invoked as /<directory-name>
│       ├── setup/                     # /setup onboarding (documents folder, CV import, or interview)
│       ├── scrape/                    # /scrape job search orchestration
│       ├── rank/                      # /rank triage scraped jobs into a ranked shortlist
│       ├── apply/                     # /apply workflow (drafter-reviewer)
│       ├── expand/                    # /expand competency enrichment from documents and online presence
│       ├── outcome/                   # /outcome record application results, archive materials
│       ├── interview/                 # /interview stage-specific prep pack + mock interview
│       ├── upskill/                   # /upskill skill gap analysis and learning plan
│       ├── gmail-sync/                # /gmail-sync auto-detect application status from Gmail
│       ├── html-report/               # /html-report generate application tracker dashboard
│       ├── notion-sync/               # /notion-sync one-way pipeline view in a Notion database
│       ├── add-template/              # /add-template register custom templates (LaTeX, Typst, ...)
│       ├── add-portal/                # /add-portal generate a job-portal search skill for your market
│       ├── reset/                     # /reset wipe profile data or documents folder
│       ├── job-application-assistant/ # Core application methodology
│       │   ├── SKILL.md               # Skill definition
│       │   ├── 01-candidate-profile.md # Your education, experience, skills
│       │   ├── 02-behavioral-profile.md# PI/DISC/personality assessment
│       │   ├── 03-writing-style.md    # Tone, structure, do's and don'ts
│       │   ├── 04-job-evaluation.md   # Scoring framework for job fit
│       │   ├── 05-cv-templates.md     # LaTeX CV structure + tailoring rules
│       │   ├── 06-cover-letter-templates.md # LaTeX cover letter templates
│       │   ├── 07-interview-prep.md   # STAR examples + interview framework
│       │   ├── 08-application-forms.md # Portal free-text fields
│       │   └── 09-web-research.md     # Fetching postings, trust boundary, 403 escalation
│       ├── jobbank-search/            # Akademikernes Jobbank (Denmark)
│       ├── jobdanmark-search/         # Jobdanmark.dk (Denmark)
│       ├── jobindex-search/           # Jobindex.dk (Denmark)
│       ├── jobnet-search/             # Jobnet.dk (Denmark, government portal)
│       ├── linkedin-search/           # LinkedIn public job listings (country-agnostic)
│       └── freehire-search/           # freehire.me tech job aggregator (multi-market, REST API)
├── CLAUDE.md                          # GENERATED: imports AGENTS.md so Claude Code picks it up
├── GEMINI.md                          # GENERATED: points Gemini CLI at AGENTS.md
├── .claude/
│   ├── skills -> ../.agents/skills    # GENERATED: symlink so Claude Code discovers the skills
│   ├── agents/                        # Claude Code subagent definitions (optional, Claude-only)
│   └── settings.json                  # Claude Code pre-approved permissions (shared, scoped)
├── cv/
│   └── main_example.tex               # moderncv LaTeX template
├── cover_letters/
│   ├── cover.cls                      # Custom cover letter LaTeX class
│   ├── cover_example.tex              # Example cover letter (structural reference + CI smoke test)
│   └── OpenFonts/                     # Lato + Raleway fonts
├── templates/                         # Custom templates registered via /add-template
│   └── README.md                      # Folder layout instructions
├── documents/                         # Career source materials for /setup Path A and /expand
│   ├── README.md                      # Folder layout instructions
│   ├── cv/                            # Master CV (PDF or .tex)
│   ├── linkedin/                      # LinkedIn profile export (PDF)
│   ├── diplomas/                      # Degree certificates and transcripts
│   ├── references/                    # Reference letters
│   └── applications/                  # Past application records (<company>_<role>/)
├── .github/workflows/ci.yml           # CI: LaTeX smoke compiles, skill lint, CLI typechecks
├── salary_lookup.py                   # Salary benchmarking tool (BYO data)
├── tools/
│   ├── check_framework_version.py     # CI check: framework_version bumped when skill files change
│   ├── check_upstream_updates.py      # Preview which personalized files an upstream update touches
│   ├── convert_salary_excel.py        # Convert salary Excel to JSON
│   ├── lint_skills.py                 # CI lint for skills, commands, settings.json
│   ├── robots_check.py                # Gate the browser-header retry against robots.txt
│   ├── security_guards.py             # CI guards: permission allowlist, gitignore rules, manifests
│   ├── upstream_triage.py             # Sort upstream commits into worth-reviewing vs probably-skip
│   ├── verify_layout.py               # Measure a compiled PDF's page layout (holes, orphans, footer collisions)
│   ├── verify_pdf.py                  # Verify a compiled PDF's page count and extractable text
│   └── README_SALARY_TOOL.md          # Salary tool setup instructions
├── job_scraper/                       # Scraper state (seen jobs, results)
├── gmail_sync/                        # /gmail-sync state (processed message IDs, last sync date)
├── upskill/                           # /upskill report output (markdown reports per run)
├── job_search_tracker.csv             # Application tracking spreadsheet
└── SETUP.md                           # Detailed setup guide
```

## How `/apply` works

The `/apply` command runs a **drafter-reviewer workflow** with mandatory PDF compilation:

1. **Parse** the job posting (URL or text)
2. **Evaluate fit** against your profile (skills, experience, culture, location, career alignment)
3. **Draft** a tailored CV and cover letter in LaTeX
4. **Spawn a reviewer agent** that researches the company and critiques the drafts
5. **Revise** based on the reviewer's feedback
6. **Compile and inspect** both PDFs: lualatex for the CV, xelatex for the cover letter. Claude reads the rendered pages and iterates on the LaTeX until the CV is exactly 2 pages with no orphaned entry titles, and the cover letter is exactly 1 page with the signature visible and fonts consistent.
7. **ATS-check the CV**: extract the PDF's text layer (`pdftotext`, optional dependency) and verify it the way an ATS parser sees it — contact details present as literal text, no garbled glyphs, sane reading order — then score the posting's keyword coverage against the extraction. Keywords the profile genuinely supports get added; genuine gaps stay visible, never stuffed.
8. **Present** the final output with a verification checklist

All claims in the CV and cover letter are verified against your actual profile. The system never fabricates skills or experience.

### What makes this workflow different

- **PDF verification loop.** Most LaTeX-resume templates produce "looks fine in the .tex" output that breaks in the PDF: job titles orphan to the next page, cover letters spill onto page 2, bullet fonts silently fall back to the body font. The `/apply` command compiles and visually inspects every PDF and applies targeted fixes (`\needspace`, `\enlargethispage`, font-matching wrappers for list items) until the layout is clean. This runs automatically on every application.
- **ATS verification on the PDF text layer.** An ATS reads the PDF's embedded text, not the rendered page — and LaTeX can silently produce PDFs whose text extracts as garbage (icon glyphs where the email should be, interleaved lines from multi-column layouts). `/apply` extracts the compiled CV's text layer with `pdftotext` and verifies contact details, reading order, and the posting's keyword coverage against what a parser actually sees. Honesty rule enforced: a keyword the profile doesn't support is acknowledged as a gap, never stuffed in.
- **Relevance-weighted CV cutting.** When a CV overflows 2 pages, the workflow does not cut mechanically from the "oldest" section. It scores each candidate line by (a) relevance to the target posting, (b) uniqueness in the document, and (c) whether the cover letter depends on it, and cuts the lowest-total-score line first. An older-role bullet that hits posting keywords survives ahead of a recent-role bullet that does not.
- **Drafter-reviewer separation.** The drafter writes; a second Claude agent, spawned with a fresh context, researches the company and critiques the drafts. The drafter then revises. This catches missed keywords, weak framing, and generic language that a single pass often leaves in.
- **Token-efficient reviewer dispatch.** The reviewer agent receives drafts inline rather than re-reading them, and the verification checklist runs once at the end of the workflow rather than being duplicated by both agents. Note: the new compile-and-inspect step in Step 5 spends some of those savings on PDF rendering and layout iteration — the workflow trades some end-to-end token cost for a real reduction in broken PDFs reaching the user.

## Customization

### Which files to edit manually

If you prefer editing files directly instead of using `/setup`:

| File | What to change |
|------|---------------|
| `AGENTS.md` | Your full profile (name, education, experience, skills, goals) |
| `01-candidate-profile.md` | Structured version of your CV data |
| `02-behavioral-profile.md` | Your behavioral assessment or self-assessment |
| `04-job-evaluation.md` | Skill match areas, career goals, motivation filters |
| `05-cv-templates.md` | Profile statement templates for different role types |
| `07-interview-prep.md` | Your STAR examples from actual experience |
| `search-queries.md` | Job search queries for your skills and location |

### Updating your search queries

As your priorities evolve, you can reconfigure just the job search without re-running the full profile setup:

```
/setup --section search
```

This re-runs the search configuration interview: which roles to target, which skills to search for, which locations, and which portals. It also suggests role types you may not have considered based on your profile.

### Custom templates

The CV uses [moderncv](https://ctan.org/pkg/moderncv) (banking style). The cover letter uses a custom `cover.cls` with Lato/Raleway fonts. Both are LaTeX — the reference engine this repo ships and maintains.

To use your own template instead — LaTeX, [Typst](https://typst.app/), or any other toolchain that compiles to PDF from the command line — run:

```
/add-template
```

Point it at your source file (a `.tex` file plus any `.cls`/`.sty` files or bundled fonts; a `.typ` file plus any local packages; or an equivalent for another toolchain). The command interviews you for the template's instructions — source extension, compile command, fonts and where they live, style rules to preserve, hard page limit — stores everything under `templates/`, runs a mandatory test compile, and activates the template so `/apply` drafts and compiles from it. Templates are stored with `[PLACEHOLDER]` tokens instead of personal data, so they're safe to commit and share.

- `/add-template --list` shows registered templates
- `/add-template --use <name>` switches between them
- `/add-template --use default` reverts to the stock moderncv / cover.cls templates

If you prefer doing it by hand, the manual route still works: update the guidance in `05-cv-templates.md` and `06-cover-letter-templates.md`.

### Job search tools

The four Danish CLI tools in `.agents/skills/` (Jobbank, Jobdanmark, Jobindex, Jobnet) demonstrate the pattern for building a job-portal integration for a specific market. If you're in a different country, run:

```
/add-portal
```

Give it your local job board's URL. The command investigates the portal (search-URL pattern, result-page structure, robots.txt/access rules), scaffolds a CLI skill with the same structure, commands, and output contract as the shipped ones, and test-runs a live query before registering anything. Auth-walled portals are declined, and portals with restrictive terms get a prominent personal-use-only warning in the generated skill. The generated skill is market-specific and lives in your fork; the generator itself is the universal part.

Maintaining a fork adapted to your market or language? Add it to the [Community forks & adaptations](https://github.com/MadsLorentzen/ai-job-search/discussions/78) thread so others can find it.

For **country-agnostic** starting points outside Denmark, the repo ships two portal skills alongside the Danish demos:

- **`linkedin-search`** — built on LinkedIn's public, unauthenticated `jobs-guest` endpoints. Field-agnostic, **zero runtime dependencies** (runs with just `bun`), and takes the search location as an explicit flag, so it works for any market out of the box (`-l "Berlin, Germany"`, `-l "Mumbai, Maharashtra, India"`, `-l "Remote"`, …). Intended for **personal use only** — automated access is against LinkedIn's Terms of Service, so keep volume low. See `.agents/skills/linkedin-search/SKILL.md`.
- **`freehire-search`** — queries the [freehire.me](https://freehire.me) aggregator's public REST API (JSON, no API key). Tech-focused (software, data, engineering, DevOps, remote), multi-market via facet flags (`--region`, `--country`, `--remote`), and **zero runtime dependencies**. Unlike the HTML-scraping Danish portals, results come back structured (skills, seniority, category). The backend is MIT-licensed and [self-hostable](https://github.com/strelov1/freehire) — point `FREEHIRE_API_URL` at your own instance if you prefer. See `.agents/skills/freehire-search/SKILL.md`.

### Extending the framework: portals, templates, criteria - and borrowing from other forks

Everything above adds up to an extension model, so here it is stated plainly. The framework has three extension points, and none of them require touching upstream:

1. **Portal skills** - the module system for job boards. Every `*-search` skill is a self-contained folder under `.agents/skills/` with the same contract (a `search`/`detail` CLI, `--format json|table|plain` output, an `enabled:` flag in its `SKILL.md`, its own tests). `/scrape` auto-discovers any installed skill that follows the contract - nothing to register, nothing to wire up. `/add-portal` generates new ones; the [community portal index](https://github.com/MadsLorentzen/ai-job-search/discussions/78) catalogs the ones other forks have built.
2. **Document templates** - `/add-template` registers any CV or cover-letter toolchain that compiles to PDF from the command line, LaTeX or otherwise.
3. **Evaluation criteria** - deal-breakers and preferences in your profile are free-form, and the evaluation rubric scores against whatever you put there. "Strong parental-leave terms", "minimum salary X per my union's scale", "no on-call" - each is one profile line, no code, and it carries real weight in `/rank` and `/apply` fit evaluations. Language is the one deal-breaker type with dedicated, structured handling: `/setup` captures every language you work in and your level (asked directly, or inferred from your CV/LinkedIn export) into a `Languages` table, and the Language Gate (`04-job-evaluation.md`) hard-rejects a posting that requires a language you haven't declared at all, while flagging - not auto-rejecting - one that asks for a higher level than you declared in a language you do work in, so a borderline case (a strict "fluent" bar against your own B1/B2, say) gets your judgment instead of a silent drop.

**Borrowing a portal skill from another fork** is the intended way to get a board that upstream doesn't ship: find it in the [portal index](https://github.com/MadsLorentzen/ai-job-search/discussions/78), open that fork, and copy the one folder into your own `.agents/skills/`. Before you run it:

- **Read the code.** All of it - these CLIs run pre-approved on your machine (`.claude/settings.json` allowlists them) against your career data. Check that the only network calls go to the job board it claims to search, that `package.json` has no `dependencies` and no lifecycle scripts (`postinstall` etc.), and that nothing reads or writes outside its own folder.
- **Run its tests offline** (`bun test` in the skill's `cli/` directory) - a well-built skill's tests pass with no network access.
- Check the `enabled:` flag and the skill's own ToS notes.

The copy step is manual on purpose. Your settings already allow installed portal skills to run without asking each time - so an installer that fetched them from third-party repos for you would skip the one check that matters: you, reading the code first. There isn't one, and that's a security decision rather than a missing feature.

Market-specific *data sources* (a national salary database, local award-rate tables) follow the same pattern as portals: they belong in a market fork, shared via [#78](https://github.com/MadsLorentzen/ai-job-search/discussions/78), not upstream.

### Salary benchmarking

The salary tool works with any salary data you provide (union statistics, Glassdoor exports, personal research, etc.). See `tools/README_SALARY_TOOL.md` for the expected format and setup. If you don't have salary data, the salary step is simply skipped.

### Starting over

To wipe your profile data and start fresh:

```
/reset profile    # clears skill files, preserves framework rules
/reset documents  # deletes files from documents/ folder
/reset all        # both
```

`/reset` shows exactly what will be deleted and requires you to type `RESET` to confirm. Nothing is deleted until you do.

### Staying up to date

Upstream moves fast. Rather than pulling raw `master` and hoping, update your fork to a tagged [release](../../releases) - a vetted checkpoint described in [CHANGELOG.md](CHANGELOG.md). `python3 tools/check_upstream_updates.py` previews exactly which of your personalized files an update touches before you merge, and `python3 tools/upstream_triage.py` sorts the commits you're behind into "worth reviewing" vs "probably skip" (a weekly workflow can post this to a rolling issue). Full walkthrough in [SETUP.md, section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork).

## Tips for better results

### Profile depth matters

The single biggest factor in output quality is how much detail you put into your profile. A thin profile produces generic applications; a detailed one enables genuinely tailored results.

- **Role descriptions:** Don't just list job titles. Describe what you actually did in each position: specific projects, tools used, responsibilities, and measurable achievements. The more material you provide, the more precisely the system can reframe your experience for different roles.
- **Skills in context:** Instead of listing "Python" or "project management," describe how and where you applied them. "Built ML pipelines for customer churn prediction in Python using scikit-learn" gives the system far more to work with than "Python, machine learning."
- **All onboarding paths work:** Whether you point `/setup` at your `documents/` folder, paste a single CV, or walk through the interview, the principle is the same: richer input produces sharper output.

### Career path discovery

The framework supports two distinct modes of job searching:

- **Explicit targeting:** You know which roles or sectors you want. The system helps refine and prioritize based on fit.
- **Latent opportunity discovery:** By analyzing your full history (not just job titles, but the actual work you did), the system can surface career paths you haven't considered. Transferable skills that map to unexpected industries, patterns in what you enjoyed or excelled at, or emerging roles that combine your domain expertise with new technology.

To get the most from this, invest time during `/setup` in describing not just your experience, but what energized you, what drained you, and what you'd want more of. This context directly shapes how the system evaluates fit and which roles it surfaces during `/scrape`.

## Contributing

Thinking about a PR? Read [CONTRIBUTING.md](CONTRIBUTING.md) first - it explains what gets merged, what lives in forks, and why.

## Acknowledgements

- [Mikkel Krogholm](https://github.com/mikkelkrogsholm) ([skills repo](https://github.com/mikkelkrogsholm/skills)) for the job search CLI skills
- Built with [Claude Code](https://claude.com/claude-code) by [Anthropic](https://anthropic.com)

## License

MIT
