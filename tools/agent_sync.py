#!/usr/bin/env python3
"""Project the canonical agent config into each runtime's expected location.

The canonical source of truth is:

    AGENTS.md          root instructions + candidate profile
    .agents/skills/    one directory per skill, each with a SKILL.md
    .agents/rules/     runtime-neutral rules

Runtimes that read those natively (Google Antigravity, Codex, Cursor, Copilot,
Jules, Aider) need nothing from this script. Runtimes that insist on their own
paths get a *projection* - a symlink, or a stub that imports the canonical file.
A projection is never a second copy of a rule, so there is nothing to keep in
sync by hand and nothing to drift.

    python3 tools/agent_sync.py            create/repair the projections
    python3 tools/agent_sync.py --check    verify them (exit 1 if stale) - CI uses this
    python3 tools/agent_sync.py --copy     real files instead of symlinks (Windows)

--copy trades the no-drift guarantee for Windows compatibility: copies are
content-compared by --check, so drift is reported rather than silently kept.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Claude Code reads CLAUDE.md and ignores AGENTS.md whenever CLAUDE.md exists
# (v2.1.277+ falls back to AGENTS.md only when there is no CLAUDE.md). An
# `@path` import works on every version, so the stub is version-proof where
# deleting CLAUDE.md would not be.
CLAUDE_STUB = """# Claude Code entry point

This workspace is runtime-neutral. The canonical instructions and candidate profile live
in [AGENTS.md](AGENTS.md); this file exists only so Claude Code imports them on every
version. **Do not add rules here** - edit `AGENTS.md` instead.

Skills are canonical under `.agents/skills/`. `.claude/skills` is a symlink onto that
directory, so `/setup`, `/scrape`, `/rank`, `/apply` and the rest resolve normally.
Run `python3 tools/agent_sync.py --check` if a skill does not show up.

@AGENTS.md
"""

GEMINI_STUB = """# Gemini CLI entry point

This workspace is runtime-neutral. The canonical instructions and candidate profile live
in AGENTS.md; read that file now and follow it. **Do not add rules here.**

Skills are canonical under `.agents/skills/` - one directory per skill with a `SKILL.md`.
To run a workflow, read `.agents/skills/<name>/SKILL.md` and follow its steps.
"""


class Projection:
    """One runtime-specific path derived from the canonical source."""

    def __init__(self, path: str, kind: str, source: str = "", content: str = ""):
        self.rel = path
        self.path = ROOT / path
        self.kind = kind          # "symlink" | "stub"
        self.source = source      # symlink target, relative to self.path's parent
        self.content = content    # stub body

    def describe(self) -> str:
        return f"{self.rel} -> {self.source}" if self.kind == "symlink" else self.rel


PROJECTIONS = [
    # Claude Code: skills must sit under .claude/skills/<name>/SKILL.md. One
    # symlink onto the canonical tree exposes every skill - including the portal
    # search CLIs, which .claude/settings.json already pre-approves but which
    # Claude Code could not discover while they lived only under .agents/.
    Projection(".claude/skills", "symlink", source="../.agents/skills"),
    Projection("CLAUDE.md", "stub", content=CLAUDE_STUB),
    Projection("GEMINI.md", "stub", content=GEMINI_STUB),
]


def canonical_ok() -> list[str]:
    problems = []
    if not (ROOT / "AGENTS.md").is_file():
        problems.append("AGENTS.md is missing - the canonical instructions file")
    skills = ROOT / ".agents" / "skills"
    if not skills.is_dir():
        problems.append(".agents/skills/ is missing - the canonical skills tree")
    elif not list(skills.glob("*/SKILL.md")):
        problems.append(".agents/skills/ holds no */SKILL.md - the tree moved")
    return problems


def check(proj: Projection, copy_mode: bool) -> str | None:
    """Return a human-readable problem, or None when the projection is intact."""
    if proj.kind == "symlink":
        target = proj.path.parent / proj.source
        if copy_mode:
            if not proj.path.is_dir():
                return f"{proj.rel} is missing (expected a copy of {proj.source})"
            diff = dircmp_differences(target, proj.path)
            return f"{proj.rel} has drifted from {proj.source}: {diff}" if diff else None
        if not proj.path.is_symlink():
            if proj.path.exists():
                return f"{proj.rel} exists but is not a symlink (re-run without --check, or use --copy)"
            return f"{proj.rel} is missing (expected a symlink to {proj.source})"
        if os.readlink(proj.path) != proj.source:
            return f"{proj.rel} points at {os.readlink(proj.path)!r}, expected {proj.source!r}"
        if not proj.path.resolve().is_dir():
            return f"{proj.rel} is a dangling symlink to {proj.source}"
        return None

    # stub
    if not proj.path.is_file():
        return f"{proj.rel} is missing"
    if proj.path.read_text(encoding="utf-8") != proj.content:
        return f"{proj.rel} differs from the generated stub (re-run tools/agent_sync.py)"
    return None


def dircmp_differences(left: Path, right: Path, prefix: str = "") -> str:
    """First difference between two trees, as a short path, or ''."""
    cmp = filecmp.dircmp(left, right)
    for name in sorted(cmp.left_only):
        return f"{prefix}{name} missing from the copy"
    for name in sorted(cmp.right_only):
        return f"{prefix}{name} is stale in the copy"
    for name in sorted(cmp.diff_files):
        return f"{prefix}{name} differs"
    for name in sorted(cmp.common_dirs):
        deeper = dircmp_differences(left / name, right / name, f"{prefix}{name}/")
        if deeper:
            return deeper
    return ""


def apply(proj: Projection, copy_mode: bool) -> str:
    if proj.kind == "stub":
        proj.path.parent.mkdir(parents=True, exist_ok=True)
        proj.path.write_text(proj.content, encoding="utf-8")
        return f"wrote   {proj.rel}"

    target = proj.path.parent / proj.source
    proj.path.parent.mkdir(parents=True, exist_ok=True)
    if proj.path.is_symlink() or proj.path.is_file():
        proj.path.unlink()
    elif proj.path.is_dir():
        shutil.rmtree(proj.path)

    if copy_mode:
        shutil.copytree(target, proj.path)
        return f"copied  {proj.describe()}"
    try:
        proj.path.symlink_to(proj.source, target_is_directory=True)
        return f"linked  {proj.describe()}"
    except OSError as exc:  # Windows without developer mode
        shutil.copytree(target, proj.path)
        return f"copied  {proj.describe()} (symlink failed: {exc})"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify only; exit 1 if a projection is stale")
    ap.add_argument("--copy", action="store_true", help="materialize real files instead of symlinks")
    args = ap.parse_args()

    broken = canonical_ok()
    if broken:
        print("agent_sync: canonical source is broken")
        for problem in broken:
            print(f"  - {problem}")
        return 1

    problems = [(p, msg) for p in PROJECTIONS if (msg := check(p, args.copy))]

    if args.check:
        if problems:
            print(f"agent_sync: {len(problems)} stale projection(s)")
            for _, msg in problems:
                print(f"  - {msg}")
            print("\nrun: python3 tools/agent_sync.py" + (" --copy" if args.copy else ""))
            return 1
        print(f"agent_sync: OK ({len(PROJECTIONS)} projections intact)")
        return 0

    if not problems:
        print(f"agent_sync: already up to date ({len(PROJECTIONS)} projections)")
        return 0
    for proj, _ in problems:
        print(apply(proj, args.copy))
    print(f"\nagent_sync: {len(problems)} projection(s) written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
