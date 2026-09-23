#!/usr/bin/env python3
"""One-command setup for the job application workspace.

    ./install.sh              (macOS / Linux)
    .\\install.ps1             (Windows)
    python3 tools/install.py  (anywhere)

Clone the repo, run it once, and every agent you have — Google Antigravity,
Claude Code, Codex, Gemini CLI, Cursor — can run the full workflow.

What it does, in order:

  1. checks prerequisites and says what each missing one costs you
  2. reports which agent runtimes it can see
  3. writes the per-runtime projections (tools/agent_sync.py)
  4. installs the portal-search CLI dependencies with bun
  5. verifies the result with tools/lint_skills.py

Nothing is installed outside this directory. The workspace is deliberately
project-scoped: skills resolve paths like `tools/rank_state.py` and `cv/`
against the repo root, and it holds your CV, tracker and documents, so a
global install would both break the skills and scatter personal data.

Flags:
  --check       verify an existing install; exit 1 if incomplete
  --copy        real files instead of symlinks (Windows without developer mode)
  --skip-deps   don't run `bun install` for the portal CLIs
  --no-color    plain output
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable or "python3"

# ---------------------------------------------------------------- presentation

class Style:
    def __init__(self, enabled: bool):
        self.on = enabled
    def _w(self, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.on else text
    def bold(self, t): return self._w("1", t)
    def dim(self, t): return self._w("2", t)
    def green(self, t): return self._w("32", t)
    def yellow(self, t): return self._w("33", t)
    def red(self, t): return self._w("31", t)
    def cyan(self, t): return self._w("36", t)


S = Style(sys.stdout.isatty() and os.environ.get("NO_COLOR") is None)
OK, WARN, BAD = "✓", "!", "✗"


def heading(n: int, title: str) -> None:
    print(f"\n{S.bold(f'{n}. {title}')}")


def line(mark: str, label: str, detail: str = "") -> None:
    colour = {OK: S.green, WARN: S.yellow, BAD: S.red}[mark]
    print(f"  {colour(mark)} {label}" + (f"  {S.dim(detail)}" if detail else ""))


# ------------------------------------------------------------- prerequisites

def which(*names: str) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


HINTS = {
    "bun": {
        "linux": "curl -fsSL https://bun.sh/install | bash",
        "darwin": "brew install oven-sh/bun/bun",
        "win32": "powershell -c \"irm bun.sh/install.ps1 | iex\"",
    },
    "latex": {
        "linux": "apt install texlive-luatex texlive-xetex texlive-latex-extra texlive-fonts-extra",
        "darwin": "brew install --cask mactex-no-gui",
        "win32": "choco install miktex",
    },
    "pdftotext": {
        "linux": "apt install poppler-utils",
        "darwin": "brew install poppler",
        "win32": "choco install poppler",
    },
}


def hint(tool: str) -> str:
    platform = "darwin" if sys.platform == "darwin" else "win32" if os.name == "nt" else "linux"
    return HINTS.get(tool, {}).get(platform, "")


def check_prerequisites() -> list[str]:
    """Report each prerequisite. Returns the list of hard failures."""
    heading(1, "Prerequisites")
    fatal: list[str] = []

    if sys.version_info >= (3, 10):
        line(OK, f"Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        line(BAD, f"Python {sys.version_info.major}.{sys.version_info.minor}", "3.10+ required")
        fatal.append("python")

    if which("bun"):
        line(OK, "bun", "portal search CLIs")
    else:
        line(WARN, "bun not found", f"portal search (/scrape) disabled — {hint('bun')}")

    if which("lualatex") and which("xelatex"):
        line(OK, "lualatex + xelatex", "CV and cover letter compilation")
    else:
        missing = " and ".join(t for t in ("lualatex", "xelatex") if not which(t))
        line(WARN, f"{missing} not found", f"you get .tex but no .pdf — {hint('latex')}")

    if which("pdftotext"):
        line(OK, "pdftotext", "ATS text-layer check")
    else:
        try:
            import pypdf  # noqa: F401
            line(OK, "pypdf", "ATS text-layer check")
        except ImportError:
            line(WARN, "pdftotext / pypdf not found",
                 f"ATS check degrades to a visual review — pip install pypdf, or {hint('pdftotext')}")

    return fatal


# ----------------------------------------------------------------- runtimes

# Best-effort detection only: nothing here gates the install, because the
# projections are cheap and make the workspace portable to a runtime installed
# later. It exists so the output tells you what will actually pick this up.
RUNTIMES = [
    ("Google Antigravity", ["antigravity"], ["~/.antigravity"],
     "reads AGENTS.md + .agents/ natively"),
    ("Claude Code", ["claude"], ["~/.claude"], "via CLAUDE.md + .claude/skills"),
    # Deliberately binary-only: Antigravity stores its own global config under
    # ~/.gemini, so treating that directory as evidence reports Gemini CLI on
    # every machine that merely has Antigravity installed.
    ("Gemini CLI", ["gemini"], [], "via GEMINI.md"),
    ("Codex", ["codex"], ["~/.codex"], "reads AGENTS.md natively"),
    ("Cursor", ["cursor"], ["~/.cursor"], "reads AGENTS.md natively"),
    ("GitHub Copilot CLI", ["copilot"], [], "reads AGENTS.md natively"),
    ("Aider", ["aider"], ["~/.aider"], "reads AGENTS.md natively"),
]


def report_runtimes() -> int:
    heading(2, "Agent runtimes")
    found = 0
    for name, commands, paths, note in RUNTIMES:
        present = bool(which(*commands)) or any(Path(p).expanduser().exists() for p in paths)
        if present:
            found += 1
            line(OK, name, note)
        else:
            # absent is not a problem: the projections are written anyway, so a
            # runtime installed later picks the workspace up with no re-run
            print(f"  {S.dim('·')} {S.dim(name + ' not detected')}")
    if not found:
        print(f"\n  {S.yellow('No agent runtime detected.')} Setup still completes — the workspace")
        print("  is plain files, so it works the moment you install one.")
    return found


# ------------------------------------------------------------------- actions

def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def sync_projections(copy: bool, check_only: bool) -> bool:
    heading(3, "Per-runtime projections")
    cmd = [PY, str(ROOT / "tools" / "agent_sync.py")]
    if check_only:
        cmd.append("--check")
    if copy:
        cmd.append("--copy")
    result = run(cmd)
    for out in result.stdout.splitlines():
        if out.strip():
            print(f"  {S.dim(out.strip())}")
    if result.returncode != 0:
        line(BAD, "projections are not in sync", result.stderr.strip()[:200])
        return False
    line(OK, "CLAUDE.md, GEMINI.md, .claude/skills")
    return True


def install_portal_deps(skip: bool, check_only: bool) -> bool:
    heading(4, "Portal search CLIs")
    clis = sorted(p for p in ROOT.glob(".agents/skills/*/cli") if (p / "package.json").is_file())
    if not clis:
        line(WARN, "no portal CLIs found", "nothing to install")
        return True
    if not which("bun"):
        line(WARN, f"{len(clis)} CLIs need bun", f"install bun, then re-run — {hint('bun')}")
        return True
    if skip:
        line(WARN, f"skipped for {len(clis)} CLIs", "--skip-deps")
        return True

    ok = True
    for cli in clis:
        name = cli.parent.name
        if check_only:
            if (cli / "node_modules").is_dir():
                line(OK, name)
            else:
                line(WARN, name, "dependencies not installed")
            continue
        result = run(["bun", "install"], cwd=cli)
        if result.returncode == 0:
            line(OK, name)
        else:
            ok = False
            line(BAD, name, result.stderr.strip().splitlines()[-1][:120] if result.stderr else "bun install failed")
    return ok


def verify() -> bool:
    heading(5, "Verify")
    result = run([PY, str(ROOT / "tools" / "lint_skills.py")])
    if result.returncode == 0:
        line(OK, result.stdout.strip() or "lint_skills OK")
        return True
    # PyYAML is the linter's only dependency and is not needed to *use* the
    # workspace, so a missing-import exit is reported as a skip, not a failure.
    if "requires PyYAML" in (result.stdout + result.stderr):
        line(WARN, "skill lint skipped", "pip install pyyaml to enable it")
        return True
    for out in result.stdout.splitlines():
        print(f"  {S.dim(out)}")
    line(BAD, "skill lint failed")
    return False


def next_steps(runtimes_found: int) -> None:
    print(f"\n{S.bold('Next steps')}")
    print(f"  1. Open this folder in your agent"
          + (f" {S.dim('(none detected — install one first)')}" if not runtimes_found else ""))
    print(f"  2. Run {S.cyan('/setup')} to build your profile"
          f" {S.dim('(or just say: run the setup skill)')}")
    print(f"  3. Then {S.cyan('/scrape')} → {S.cyan('/rank')} → {S.cyan('/apply <url>')}")
    print(f"\n  Docs: {S.dim('README.md')} · runtime contract: {S.dim('AGENTS.md')}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--check", action="store_true", help="verify an existing install")
    ap.add_argument("--copy", action="store_true", help="copies instead of symlinks (Windows)")
    ap.add_argument("--skip-deps", action="store_true", help="skip bun install")
    ap.add_argument("--no-color", action="store_true", help="plain output")
    args = ap.parse_args()

    if args.no_color:
        S.on = False

    mode = "Verifying" if args.check else "Setting up"
    print(S.bold(f"{mode} the job application workspace"))
    print(S.dim(f"  {ROOT}"))

    fatal = check_prerequisites()
    if fatal:
        print(f"\n{S.red('Cannot continue:')} Python 3.10+ is required.")
        return 1

    runtimes_found = report_runtimes()
    steps = [
        sync_projections(args.copy, args.check),
        install_portal_deps(args.skip_deps, args.check),
        verify(),
    ]

    if not all(steps):
        verb = "incomplete" if args.check else "finished with errors"
        print(f"\n{S.red(BAD)} Install {verb}. See the lines marked {S.red(BAD)} above.")
        if args.check:
            print(f"  Run {S.cyan('./install.sh')} to repair.")
        return 1

    print(f"\n{S.green(OK)} {S.bold('Ready.')}" if not args.check
          else f"\n{S.green(OK)} {S.bold('Install is complete.')}")
    if not args.check:
        next_steps(runtimes_found)
    return 0


if __name__ == "__main__":
    sys.exit(main())
