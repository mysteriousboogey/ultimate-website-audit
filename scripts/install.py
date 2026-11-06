#!/usr/bin/env python3
"""Copy this portable skill to an explicitly selected, new directory."""
import argparse
import shutil
import sys
from pathlib import Path


def install(destination):
    if sys.version_info < (3, 10):
        raise ValueError('Python 3.10 or newer is required')
    source = Path(__file__).resolve().parents[1]
    target = Path(destination).expanduser().absolute()
    if target.exists() or target.is_symlink():
        raise ValueError('Destination already exists; choose a new directory. Nothing was overwritten.')
    if target.resolve().is_relative_to(source):
        raise ValueError('Choose a destination outside this source folder')
    # Claim the destination first so an existing installation cannot be overwritten.
    target.mkdir(parents=True, exist_ok=False)
    try:
        for filename in ('SKILL.md', 'README.md'):
            shutil.copy2(source / filename, target / filename)
        for directory in ('references', 'scripts', 'examples'):
            shutil.copytree(source / directory, target / directory,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    except Exception:
        shutil.rmtree(target)
        raise
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', required=True, help="Host's documented destination for the complete skill folder")
    args = parser.parse_args()
    try:
        print('Installed skill files at ' + str(install(args.dest)))
        print("Reload your assistant and verify skill discovery using the host's instructions.")
    except (OSError, ValueError) as exc:
        sys.exit('Installation failed: ' + str(exc))
