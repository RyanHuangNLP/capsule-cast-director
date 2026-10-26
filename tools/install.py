#!/usr/bin/env python3
"""Install a self-contained copy of the skill, refusing to overwrite a target."""

import argparse
import shutil
import sys
from pathlib import Path

NAME = "directing-capsule-casts"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / NAME


def install(destination):
    destination = Path(destination).expanduser().absolute()
    target = destination / NAME
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Already exists: {target}. No files were changed.")
    if not (SOURCE / "SKILL.md").is_file() or not (SOURCE / "LICENSE").is_file():
        raise FileNotFoundError("The source skill or its license is missing.")
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents" / "skills",
                        help="parent skill directory (default: ~/.agents/skills)")
    args = parser.parse_args(argv)
    try:
        target = install(args.dest)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Installed {NAME} at {target}")
    print("If the skill does not appear in your client, reload or restart the client.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
