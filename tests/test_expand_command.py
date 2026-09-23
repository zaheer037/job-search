"""Tests for the /expand command specification."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPAND_COMMAND_FILE = REPO_ROOT / ".agents" / "skills" / "expand" / "SKILL.md"


class ExpandCommandTests(unittest.TestCase):
    def test_expand_skill_file_exists(self):
        self.assertTrue(
            EXPAND_COMMAND_FILE.exists(),
            "expand/SKILL.md must exist under .agents/skills/",
        )

    def test_expand_skill_file_has_portable_frontmatter(self):
        """The portable Agent Skills format opens every SKILL.md with YAML, and
        lint_skills.py enforces that `name` equals the directory."""
        text = EXPAND_COMMAND_FILE.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"), "SKILL.md must open with YAML frontmatter")
        self.assertIn("\nname: expand\n", text, "frontmatter name must be 'expand'")
        self.assertIn("# /expand", text, "the '# /expand' heading documents the invocation")

    def test_expand_covers_all_discovery_sources(self):
        text = EXPAND_COMMAND_FILE.read_text(encoding="utf-8")
        sources = [
            "documents/cv/",
            "documents/linkedin/",
            "documents/diplomas/",
            "documents/references/",
            "GitHub Profile",
        ]
        for src in sources:
            self.assertIn(src, text, f"expand.md must include discovery source: {src}")

    def test_expand_maps_github_projects_to_independent_projects_section(self):
        text = EXPAND_COMMAND_FILE.read_text(encoding="utf-8")
        self.assertIn("## Independent Projects", text)
        self.assertIn("Independent Projects & Portfolio", text)
        self.assertIn("GitHub — repo-name", text)
        self.assertIn("Portfolio & projects grounded in code", text)
        self.assertNotIn("documents/projects/", text)

    def test_expand_enforces_additive_and_confirmation_principles(self):
        text = EXPAND_COMMAND_FILE.read_text(encoding="utf-8")
        self.assertIn("Additive only", text)
        self.assertIn("User confirms before writing", text)
        self.assertIn("`all`", text)
        self.assertIn("`review`", text)
        self.assertIn("`skip`", text)


if __name__ == "__main__":
    unittest.main()

