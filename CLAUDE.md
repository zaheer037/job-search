# Claude Code entry point

This workspace is runtime-neutral. The canonical instructions and candidate profile live
in [AGENTS.md](AGENTS.md); this file exists only so Claude Code imports them on every
version. **Do not add rules here** - edit `AGENTS.md` instead.

Skills are canonical under `.agents/skills/`. `.claude/skills` is a symlink onto that
directory, so `/setup`, `/scrape`, `/rank`, `/apply` and the rest resolve normally.
Run `python3 tools/agent_sync.py --check` if a skill does not show up.

@AGENTS.md
