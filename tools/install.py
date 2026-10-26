#!/usr/bin/env python3
"""Install a self-contained copy of the skill, refusing to overwrite a target."""

import argparse
import shutil
import sys
from pathlib import Path

NAME = "directing-capsule-casts"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / NAME


def install(destination):
    destination = Path(destination).expanduser().resolve()
    target = destination / NAME
    source = SOURCE.resolve()
    if target == source or source in target.parents:
        raise ValueError("Choose a destination outside the source skill directory.")
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Already exists: {target}. No files were changed.")
    if not (source / "SKILL.md").is_file() or not (source / "LICENSE").is_file():
        raise FileNotFoundError("The source skill or its license is missing.")
    destination.mkdir(parents=True, exist_ok=True)
    target.mkdir()
    try:
        shutil.copytree(source, target, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    except BaseException:
        shutil.rmtree(target, ignore_errors=True)
        raise
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents" / "skills",
                        help="parent skill directory (default: ~/.agents/skills)")
    args = parser.parse_args(argv)
    try:
        target = install(args.dest)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Installed {NAME} at {target}")
    print("If the skill does not appear in your client, reload or restart the client.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
