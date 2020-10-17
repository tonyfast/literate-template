""" deathbeds literate template meta-automation
"""
import shutil
from doit.tools import config_changed
from doit.action import CmdAction
import subprocess
import sys
import json
import os
from pathlib import Path

DOIT_CONFIG = {"backend": "sqlite3", "verbosity": 2, "par_type": "thread"}

HERE = Path(__file__).parent

CCJ = HERE / "cookiecutter.json"
TMPL = HERE / "{{ cookiecutter.name }}"
TMPL_FILES = [f for f in TMPL.rglob("*") if not f.is_dir()]

PROJ = HERE / "untitled"
PROJ_PROJ = PROJ / "pyproject.toml"
BUILD = HERE / "build"
BUILD.exists() or BUILD.mkdir()
PIP_FROZEN = BUILD / "pip-freeze.log"
ENV_OK = BUILD / "env.ok"

CC_USE_MAMBA = bool(json.loads(os.environ.get("CC_USE_MAMBA", "false")))

ENV_YML = PROJ / "binder" / "environment.yml"


def task_test():
    yield dict(
        name="cc",
        file_dep=TMPL_FILES,
        actions=[
            lambda: shutil.rmtree(PROJ) if PROJ.exists() else None,
            ["cookiecutter", ".", "-f", "--no-input"],
        ],
        targets=[PROJ_PROJ],
    )

    if CC_USE_MAMBA:
        yield dict(
            name="env",
            file_dep=[ENV_YML],
            actions=[
                CmdAction(
                    ["mamba", "env", "update", "--prefix", os.environ["CONDA_PREFIX"], "--file", ENV_YML], cwd=PROJ, shell=False
                ),
                lambda: ENV_OK.touch(),
            ],
        )
    else:
        yield dict(
            name="env",
            file_dep=[PROJ_PROJ],
            actions=[
                CmdAction(
                    ["python", "-m", "pip", "install", "-e", ".[dev]"], shell=False
                ),
                lambda: ENV_OK.touch(),
            ],
        )

    yield dict(
        name="setup",
        file_dep=[ENV_OK, PROJ_PROJ],
        actions=[
            _pip(["install", "-e", ".[dev]", "--ignore-installed", "-vv"]),
            _log([sys.executable, "-m", "pip", "freeze"], PIP_FROZEN),
        ],
    )

    yield dict(name="doit", file_dep=[PIP_FROZEN], actions=[_doit()])


def _pip(args):
    return CmdAction([sys.executable, "-m", "pip", *args], cwd=PROJ, shell=False)


def _doit(args=[]):
    return CmdAction([sys.executable, "-m", "doit", *args], cwd=PROJ, shell=False)


def _log(args, path, **kwargs):
    def _run():
        if not path.parent.exists():
            path.parent.mkdir(exist_ok=True)
        path.write_bytes(subprocess.check_output(args, **kwargs))

    return _run
