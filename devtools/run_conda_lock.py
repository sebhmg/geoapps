#!/usr/bin/env python3

#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

"""
Creates cross platform lock files for each python version and per-platform conda environment files.

Cross platform lock files are created at the root of the project.
Per-platform conda environment files with and without dev dependencies, are placed under the `environments` sub-folder.
They include an environment file for Python 3.9 with fewer dependencies for simpeg.

Usage: from a the conda base environment, at the root of the project:
> python devtools/run_conda_lock.py

To prepare the conda base environment, see devtools/setup-conda-base.bat
"""

import os
import subprocess
from contextlib import contextmanager
from pathlib import Path

from add_url_tag_sha256 import patchPyprojectToml

env_file_variables_section_ = """
variables:
  KMP_WARNINGS: 0
"""

_environments_folder = Path("environments")


@contextmanager
def print_execution_time(name: str = "") -> None:
    from datetime import datetime

    start = datetime.now()
    try:
        yield
    finally:
        duration = datetime.now() - start
        message_prefix = f" {name} -" if name else ""
        print(f"--{message_prefix} execution time: {duration}")


def create_multi_platform_lock(py_ver: str, platform: str = None) -> None:
    print(f"# Creating multi-platform lock file for Python {py_ver} ...")
    platform_option = f"-p {platform}" if platform else ""
    with print_execution_time(f"conda-lock for {py_ver}"):
        subprocess.run(
            f"conda-lock lock --mamba --no-micromamba -f pyproject.toml -f {_environments_folder}/env-python-{py_ver}.yml {platform_option} --lockfile conda-py-{py_ver}-lock.yml",
            env=dict(os.environ, PYTHONUTF8="1"),
            shell=True,
            check=True,
            stderr=subprocess.STDOUT,
        )


def per_platform_env(py_ver: str, full=True, dev=False, suffix="") -> None:
    print(
        f"# Creating per platform Conda env files for Python {py_ver} ({'WITH' if dev else 'NO'} dev dependencies) ... "
    )
    dev_dep_option = "--dev-dependencies" if dev else "--no-dev-dependencies"
    dev_suffix = "-dev" if dev else ""
    extras_option = "--extras full" if full else ""
    subprocess.run(
        (
            f"conda-lock render {dev_dep_option} {extras_option} -k env"
            f" --filename-template {_environments_folder}/conda-py-{py_ver}-{{platform}}{dev_suffix}{suffix}.lock conda-py-{py_ver}-lock.yml"
        ),
        env=dict(os.environ, PYTHONUTF8="1"),
        shell=True,
        check=True,
        stderr=subprocess.STDOUT,
    )
    platform_glob = "*-64"
    for lock_env_file in _environments_folder.glob(
        f"conda-py-{py_ver}-{platform_glob}{dev_suffix}{suffix}.lock.yml"
    ):
        with open(lock_env_file, "a") as f:
            f.write(env_file_variables_section_)


def config_conda() -> None:
    subprocess.run(
        "conda config --set channel_priority strict",
        shell=True,
        check=True,
        stderr=subprocess.STDOUT,
    )


def delete_existing_files() -> None:
    if _environments_folder.exists():
        for f in _environments_folder.glob("*.lock.yml"):
            f.unlink()

    for f in Path().glob("*-lock.yml"):
        f.unlink()


if __name__ == "__main__":
    assert _environments_folder.is_dir()
    delete_existing_files()

    config_conda()

    patchPyprojectToml()
    with print_execution_time(f"run_conda_lock"):
        for py_ver in ["3.9", "3.8", "3.7"]:
            create_multi_platform_lock(py_ver)
            per_platform_env(py_ver, dev=False)
            per_platform_env(py_ver, dev=True)
