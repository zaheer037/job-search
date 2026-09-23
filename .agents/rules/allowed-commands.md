# Commands this workspace expects to run

The canonical allowlist. `.claude/settings.json` mirrors it for Claude Code; mirror it into
your own runtime's allowlist to skip per-command approval prompts. Anything outside this
list should still prompt — that is the point of the list being short.

## Portal search CLIs (need [bun](https://bun.sh))

```
bun run .agents/skills/jobbank-search/cli/src/cli.ts <args>
bun run .agents/skills/jobdanmark-search/cli/src/cli.ts <args>
bun run .agents/skills/jobindex-search/cli/src/cli.ts <args>
bun run .agents/skills/jobnet-search/cli/src/cli.ts <args>
bun run .agents/skills/linkedin-search/cli/src/cli.ts <args>
bun run .agents/skills/freehire-search/cli/src/cli.ts <args>
```

## Helper scripts (stdlib Python, no install)

```
python3 salary_lookup.py <args>          salary benchmarks
python3 tools/rank_state.py <args>       query/update scraper state without loading it into context
python3 tools/job_key.py <args>          stable dedup key for a posting
python3 tools/verify_pdf.py <args>       page count, text-layer extraction, keyword checks
python3 tools/verify_layout.py <args>    orphaned-title and page-break checks
python3 tools/agent_sync.py [--check]    create/verify the per-runtime projections
python3 tools/lint_skills.py             validate the skill tree
```

## Document toolchain

```
lualatex -interaction=nonstopmode -halt-on-error <file>.tex    CVs
xelatex  -interaction=nonstopmode -halt-on-error <file>.tex    cover letters
pdftotext -layout -enc UTF-8 <file>.pdf                        ATS text layer
pdftoppm -png -r 110 <file>.pdf page                           PDF -> PNG, for runtimes whose file read cannot display a PDF
```

A custom template registered through `/add-template` declares its own compile command; use
that instead of the two above.
