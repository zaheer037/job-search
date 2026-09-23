#!/usr/bin/env sh
# One-command setup for the job application workspace.
#
#   ./install.sh              set everything up
#   ./install.sh --check      verify an existing install
#   ./install.sh --copy       copies instead of symlinks
#
# Everything real happens in tools/install.py; this only locates a Python 3.10+
# interpreter, so the repo stays runnable on a machine where `python3` is absent
# but `python` is a modern 3.x (common on Windows and some minimal images).
set -eu

cd "$(dirname "$0")"

for candidate in python3 python python3.13 python3.12 python3.11 python3.10; do
    if command -v "$candidate" >/dev/null 2>&1 &&
       "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
        exec "$candidate" tools/install.py "$@"
    fi
done

echo "Python 3.10+ is required and was not found on PATH." >&2
echo "Install it from https://www.python.org/downloads/ and re-run ./install.sh" >&2
exit 1
