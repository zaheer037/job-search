"""Guards for the one-command installer and the template predicate.

The installer is the first thing a new user runs, so its failure modes matter
more than its happy path: it must refuse to claim success when a projection is
missing, and it must not report an agent runtime that is not installed (the
first draft reported Gemini CLI on every machine that merely had Antigravity,
because both store config under ~/.gemini).

is_template() replaced a `github.repository == '<owner>/<repo>'` gate that
silently disabled the placeholder-integrity guard in every repo but the
original - including a fork republished as a template, which is exactly where
committed personal data does the most damage.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INSTALL = REPO / "tools" / "install.py"
IS_TEMPLATE = REPO / "tools" / "is_template.py"

sys.path.insert(0, str(REPO))
from tools.is_template import SENTINEL, is_template  # noqa: E402


def run(script: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args], capture_output=True, text=True, cwd=cwd
    )


class InstallerEntryPoints(unittest.TestCase):
    def test_install_sh_is_executable(self):
        script = REPO / "install.sh"
        self.assertTrue(script.is_file(), "install.sh is the documented one command")
        self.assertTrue(script.stat().st_mode & 0o111, "install.sh must be executable in git")

    def test_windows_wrapper_exists(self):
        self.assertTrue((REPO / "install.ps1").is_file(), "Windows users need install.ps1")

    def test_windows_wrapper_defaults_to_copy_mode(self):
        """Windows blocks symlinks without Developer Mode, so the wrapper must
        pass --copy unless the user opts back in."""
        text = (REPO / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("--copy", text)
        self.assertIn("Symlink", text, "there must be an opt-out back to symlinks")

    def test_readme_documents_the_command(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("./install.sh", readme, "the one command must be in the README")


class InstallerCheckMode(unittest.TestCase):
    def test_check_passes_on_a_healthy_repo(self):
        result = run(INSTALL, "--check", "--skip-deps", "--no-color")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_fails_when_a_projection_is_missing(self):
        """--check must not report success just because the files are on disk;
        a missing projection means some runtime silently sees no skills."""
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        clone = work / "repo"
        shutil.copytree(REPO, clone, symlinks=True, ignore=shutil.ignore_patterns(".git"))
        (clone / "CLAUDE.md").unlink()

        result = run(clone / "tools" / "install.py", "--check", "--skip-deps", "--no-color")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("CLAUDE.md", result.stdout)

    def test_runtime_detection_does_not_invent_runtimes(self):
        """Every runtime row is either detected or explicitly 'not detected' -
        no row may be silently dropped, which would hide a supported runtime."""
        result = run(INSTALL, "--check", "--skip-deps", "--no-color")
        for name in ("Google Antigravity", "Claude Code", "Gemini CLI", "Codex", "Cursor"):
            self.assertIn(name, result.stdout, f"{name} missing from the runtime report")

    def test_gemini_cli_is_detected_by_binary_only(self):
        """~/.gemini belongs to Antigravity too, so it is not evidence of Gemini CLI."""
        from tools.install import RUNTIMES

        row = next(r for r in RUNTIMES if r[0] == "Gemini CLI")
        self.assertEqual(row[2], [], "Gemini CLI must not be detected from a shared directory")


class TemplatePredicate(unittest.TestCase):
    def test_pristine_repo_reports_template(self):
        self.assertTrue(is_template(), "this checkout still carries the placeholders")
        result = run(IS_TEMPLATE)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "template")

    def test_personalized_copy_reports_personalized(self):
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        (work / "tools").mkdir()
        shutil.copy(IS_TEMPLATE, work / "tools" / "is_template.py")
        (work / "AGENTS.md").write_text(
            (REPO / "AGENTS.md").read_text(encoding="utf-8").replace(SENTINEL, "Jane Doe"),
            encoding="utf-8",
        )

        result = run(work / "tools" / "is_template.py")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.strip(), "personalized")

    def test_missing_profile_fails_closed(self):
        """A broken checkout must not read as 'template' - that would leave the
        guards on with nothing to guard, or off with everything to guard."""
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        (work / "tools").mkdir()
        shutil.copy(IS_TEMPLATE, work / "tools" / "is_template.py")

        result = run(work / "tools" / "is_template.py")

        self.assertEqual(result.returncode, 1)

    def test_quiet_mode_prints_nothing(self):
        result = run(IS_TEMPLATE, "--quiet")
        self.assertEqual(result.stdout.strip(), "")
        self.assertEqual(result.returncode, 0)


class CiGatesAreRepoAgnostic(unittest.TestCase):
    """The whole point of is_template.py: a fork republished as a template for
    other people to clone must keep the guards that protect personal data."""

    def setUp(self):
        self.ci = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    def test_no_hardcoded_owner_gate_remains(self):
        self.assertNotIn(
            "github.repository ==",
            self.ci,
            "an owner-name gate disables the guard in every other template repo",
        )

    def test_guarded_steps_use_the_template_predicate(self):
        self.assertGreaterEqual(
            self.ci.count("tools/is_template.py --quiet"),
            3,
            "the framework-version, stock-PDF and placeholder-integrity gates "
            "must all be content-based",
        )


if __name__ == "__main__":
    unittest.main()
