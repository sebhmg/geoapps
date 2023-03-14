#!/usr/bin/env python3

#  Copyright (c) 2021-2023 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

_max_lines = 10

"""
This script checks that the copyright year is up to date in all files,
with the option to auto-patch files with the added date from git and current date.

To auto-patch files, set environment variable UPDATE_COPYRIGHT_YEAR=true.
If a start date was already present and older that the git added date,
it will preserve that one.
"""


def git_last_added_year(file: Path):
    """
    Get the year of the last commit that added the file.
    :param file: Path to the file.
    """

    return subprocess.check_output(
        f"git log -1 --format=%ad --date=format:%Y --diff-filter=A {file}",
        shell=True,
        encoding="utf-8",
    ).strip()


def _years_text(git_added_year: int, start_year: int, end_year: int) -> str:
    """
    Get the text to use for the copyright year range.

    If the `start_year` is older than `git_added_year, use `start_year`.
    If the resulting start year is the same as end_year, return only the end year.

    :param git_added_year: The year the file was added to git.
    :param start_year: The start year of the range already in the file (or the copyright date if not a range).
    :param end_year: The desired end of year (typically the current year).
    :return: The text to use for the copyright year range.
        Examples:
        - (2021, 2021, 2023) -> 2021-2023
        - (2020, 2021, 2023) -> 2020-2023
        - (2021, 2020, 2023) -> 2020-2023
    """

    start_year = min(git_added_year, start_year)
    if start_year == end_year:
        return str(end_year)
    return f"{start_year}-{end_year}"


def patch_copyright_year(temp_dir: Path, file: Path, current_year: int) -> bool:
    """
    Patch the copyright year in the file if needed.
    :param temp_dir: Temporary directory to use for the patched file.
    :param file: Path to the file to patch.
    :param current_year: The current year.
    :return: True if the file was patched, False otherwise.
    """

    copyright_re = re.compile(
        rf"^(.*\bcopyright \(c\)\s)(\d{{4}})(:?-\d{{4}}|)\s", re.IGNORECASE
    )

    copyright_line_idx = None
    patched_line = None
    with open(file, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i > _max_lines:
                break

            match = copyright_re.match(line)
            if match is not None:
                git_year = git_last_added_year(file)
                replacement = (
                    lambda m: m[1]
                    + _years_text(int(git_year), int(m[2]), current_year)
                    + " "
                )
                patched_line = copyright_re.sub(replacement, line)
                if patched_line != line:
                    copyright_line_idx = i
                break

    if copyright_line_idx is None:
        return False

    assert patched_line is not None
    patched_file = temp_dir / file.name
    with open(patched_file, encoding="utf-8", mode="w") as patched:
        with open(file, encoding="utf-8") as input:
            for i, line in enumerate(input):
                if i != copyright_line_idx:
                    patched.write(line)
                else:
                    patched.write(patched_line)
    os.replace(patched_file, file)
    return True


def main(update_year: bool = False):
    """
    Check that the copyright year is up to date in all files.
    Optionally, auto-patch files with the added date from git and current date.

    :param update_year: If True, auto-patch files with the added date from git and current date.
    """
    current_year = date.today().year
    copyright_re = re.compile(
        rf"\bcopyright \(c\)\s(:?\d{{4}}-|){current_year}\s", re.IGNORECASE
    )
    files = sys.argv[1:]
    report_files = []
    patched_files = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for f in files:
            if update_year and patch_copyright_year(
                temp_dir=Path(temp_dir), file=Path(f), current_year=current_year
            ):
                patched_files.append(f)
                continue

            with open(f, encoding="utf-8") as file:
                has_dated_copyright = False
                for i, line in enumerate(file):
                    if i >= _max_lines and not f.endswith("README.rst"):
                        break
                    if re.search(copyright_re, line):
                        has_dated_copyright = True
                        break

                if not has_dated_copyright:
                    report_files.append(f)

    for f in report_files:
        sys.stderr.write(f"{f}: No copyright or invalid year\n")
    for f in patched_files:
        sys.stderr.write(f"{f}: Patched with updated copyright year\n")

    if len(report_files) > 0:
        exit(1)


if __name__ == "__main__":
    # read environment UPDATE_COPYRIGHT_YEAR true or false, false by default
    update_year = (
        os.environ.get("UPDATE_COPYRIGHT_YEAR", "false").strip().lower() == "true"
    )

    main(update_year)
