#!/usr/bin/env python3
"""Lint the repo's skill and settings files.

Run from anywhere: python tools/lint_skills.py

Checks:
- Every SKILL.md (.agents/skills/*, plus any legacy .claude/skills/*) has YAML
  frontmatter that parses, with non-empty `name` and `description` keys
- A skill's directory name equals its frontmatter `name`. Runtimes disagree about
  which one backs the `/<skill>` command - Antigravity documents the directory,
  Claude Code uses the frontmatter - so a mismatch means the same workspace
  exposes a workflow under two different names depending on who reads it
- `allowed-tools` entries of the form `Bash(bun run <path> *)` point at files
  that exist (skill paths resolve relative to the repo root and to .agents/)
- .claude/settings.json is valid JSON with a permissions.allow list
- The per-runtime projections are intact (delegates to tools/agent_sync.py)

Exit code 0 on success, 1 with a failure list otherwise.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("lint_skills.py requires PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{rel(path)}: missing YAML frontmatter (file must start with ---)")
        return
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{rel(path)}: unterminated YAML frontmatter")
        return
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        errors.append(f"{rel(path)}: frontmatter is not valid YAML: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: frontmatter did not parse to a mapping")
        return
    for key in ("name", "description"):
        if not data.get(key):
            errors.append(f"{rel(path)}: frontmatter missing required key '{key}'")

    name = data.get("name")
    directory = path.parent.name
    if name and str(name) != directory:
        errors.append(
            f"{rel(path)}: frontmatter name {str(name)!r} does not match directory "
            f"{directory!r} - the skill would be /{name} on some runtimes and "
            f"/{directory} on others; rename the directory to match"
        )

    allowed = data.get("allowed-tools", "")
    if isinstance(allowed, str):
        for match in re.finditer(r"bun run ([^\s)]+)", allowed):
            target = match.group(1).rstrip("*")
            if not target or target.endswith("/"):
                continue
            # Targets may contain globs (e.g. .agents/skills/*/cli/src/cli.ts);
            # require at least one existing file to match.
            if "*" in target:
                if not list(ROOT.glob(target)) and not list((ROOT / ".agents").glob(target)):
                    errors.append(f"{rel(path)}: allowed-tools glob matches no files: {target}")
            else:
                candidates = [ROOT / target, ROOT / ".agents" / target]
                if not any(c.is_file() for c in candidates):
                    errors.append(f"{rel(path)}: allowed-tools references a missing file: {target}")


def check_settings() -> None:
    path = ROOT / ".claude" / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f".claude/settings.json: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(".claude/settings.json: expected top-level JSON value to be an object")
        return
    permissions = data.get("permissions", {})
    if not isinstance(permissions, dict):
        errors.append(".claude/settings.json: expected permissions to be an object")
        return
    if not isinstance(permissions.get("allow"), list):
        errors.append(".claude/settings.json: expected permissions.allow to be a list")


def check_projections() -> None:
    """The per-runtime projections are agent_sync.py's contract, not ours -
    delegate so there is one definition of "intact". Skipped in fixture repos
    that carry no canonical tree."""
    sync = ROOT / "tools" / "agent_sync.py"
    if not sync.is_file() or not (ROOT / "AGENTS.md").is_file():
        return
    result = subprocess.run([sys.executable, str(sync), "--check"], capture_output=True, text=True)
    if result.returncode != 0:
        reported = [l.strip()[2:] for l in result.stdout.splitlines() if l.strip().startswith("- ")]
        for line in reported:
            errors.append(f"projection: {line}")
        if not reported:
            errors.append("projection: tools/agent_sync.py --check failed")


def main() -> int:
    # .claude/skills is normally a symlink onto .agents/skills, so the two globs
    # return the same files twice - dedupe by resolved path.
    found: dict[Path, Path] = {}
    for pattern in (".agents/skills/*/SKILL.md", ".claude/skills/*/SKILL.md"):
        for path in sorted(ROOT.glob(pattern)):
            found.setdefault(path.resolve(), path)
    skills = [found[key] for key in sorted(found)]

    if not skills:
        errors.append("no SKILL.md files found - glob roots are wrong or the tree moved")

    for skill in skills:
        check_skill(skill)
    check_settings()
    check_projections()

    if errors:
        print(f"lint_skills: {len(errors)} failure(s)")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"lint_skills: OK ({len(skills)} skills, settings.json, projections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
