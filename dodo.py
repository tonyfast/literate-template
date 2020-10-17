""" deathbeds literate template meta-automation
"""
from pathlib import Path

HERE = Path(__file__).parent

CCJ = HERE / "cookiecutter.json"
PROJ = HERE / "{{ cookiecutter.name }}"
PROJ_FILES = [f for f in PROJ.rglob("*") if not f.is_dir()]


def task_test():
    return dict(
        file_dep=PROJ_FILES, actions=[["cookiecutter", ".", "-f", "--no-input"]]
    )
