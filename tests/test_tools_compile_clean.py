"""Every Python file must compile without a SyntaxWarning.

`tools/verify_layout.py` documented a LaTeX fix in its module docstring and wrote
`\\hypersetup{...}` with a single backslash. Python read `\\h` as an escape it does
not recognise, so CPython emitted

    SyntaxWarning: invalid escape sequence '\\h'

on the *first* run of the tool in each interpreter - on stderr, ahead of the tool's
own output. Nothing failed, which is why it survived: the exit code stayed 0 and the
measurements were right. But these tools are invoked by an agent that reads their
stderr to decide whether a step worked, and a warning that looks like a diagnostic
is exactly the kind of noise that gets a clean run misread as a broken one. From
Python 3.12 the same construct is a DeprecationWarning slated to become a
SyntaxError, so the docstrings carrying LaTeX - which is most of them, in a repo
built on LaTeX templates - have to be raw strings.

The check is repo-wide rather than per-file because the failure mode is a property
of writing LaTeX in a docstring, and every tool here is a candidate for it.
"""

import unittest
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Vendored dependencies are not ours to fix; everything else is.
SKIP_PARTS = {"node_modules", ".venv", "venv", ".git", "__pycache__"}


def python_sources() -> list[Path]:
    return sorted(
        p
        for p in REPO.rglob("*.py")
        if not SKIP_PARTS & set(p.parts)
    )


class SourcesCompileWithoutWarnings(unittest.TestCase):
    def test_every_python_file_compiles_cleanly(self):
        sources = python_sources()
        self.assertGreater(len(sources), 20, "glob root is wrong - the tree moved")

        offenders = []
        for path in sources:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                try:
                    compile(path.read_text(encoding="utf-8"), str(path), "exec")
                except SyntaxError as exc:  # pragma: no cover - would break everything
                    offenders.append(f"{path.relative_to(REPO)}: SyntaxError: {exc}")
                    continue
            for entry in caught:
                if issubclass(entry.category, (SyntaxWarning, DeprecationWarning)):
                    offenders.append(
                        f"{path.relative_to(REPO)}: {entry.category.__name__}: {entry.message}"
                    )

        self.assertEqual(
            offenders,
            [],
            "compile-time warnings reach stderr before a tool's own output and get "
            "misread as failures. A docstring containing LaTeX needs an r-prefix:\n  "
            + "\n  ".join(offenders),
        )


class LatexCarryingDocstringsAreRaw(unittest.TestCase):
    """The specific shape of the bug, pinned so a fix cannot silently regress."""

    def test_verify_layout_docstring_is_raw(self):
        text = (REPO / "tools" / "verify_layout.py").read_text(encoding="utf-8")
        self.assertIn(
            'r"""',
            text.split("\n\n")[0],
            "verify_layout.py's module docstring quotes LaTeX control sequences, so "
            "it must be an r-string",
        )


if __name__ == "__main__":
    unittest.main()
