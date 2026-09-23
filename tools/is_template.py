#!/usr/bin/env python3
"""Is this working copy still a pristine template, or has someone's profile landed in it?

    python3 tools/is_template.py           prints "template" or "personalized"
    python3 tools/is_template.py --quiet   no output; exit 0 = template, 1 = personalized

Several guards only make sense on an unpersonalized copy: the placeholder-integrity
check (which exists to catch personal data committed to a public template), the
stock-PDF content assertions, and the framework_version bump gate.

Those used to be gated on `github.repository == '<original owner>/<repo>'`, which
silently disabled every one of them in any other template repo - including a fork
republished for other people to clone, which is exactly where a leaked name or
address does the most damage. Gating on the *content* instead is both
repo-agnostic and closer to the actual intent: run the guard while there is still
a placeholder to protect, and stand down once the user has run /setup.

`[YOUR_NAME]` in AGENTS.md is the sentinel. /setup replaces it in the Identity
block it populates, so its absence is a reliable signal that a real profile is
present.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SENTINEL = "[YOUR_NAME]"
PROFILE = ROOT / "AGENTS.md"


def is_template() -> bool:
    try:
        return SENTINEL in PROFILE.read_text(encoding="utf-8")
    except OSError:
        # No AGENTS.md at all is not a pristine template - fail closed so a
        # broken checkout does not quietly switch the guards off.
        return False


def main() -> int:
    template = is_template()
    if "--quiet" not in sys.argv:
        print("template" if template else "personalized")
    return 0 if template else 1


if __name__ == "__main__":
    sys.exit(main())
