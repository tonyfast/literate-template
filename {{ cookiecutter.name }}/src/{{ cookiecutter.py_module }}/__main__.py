""" top-level data for {{ cookiecutter.py_module }}
"""
# Copyright (c) 2020 {{ cookiecutter.author }}
# Distributed under the terms of the BSD-3-Clause License

import json
from pathlib import Path

from ._version import __version__


def _jupyter_labextension_paths():
    package = Path(__file__).parent.resolve() / "static" / "package.json"
    data = json.loads(package.read_text(encoding="utf-8"))

    return [{"src": "static", "dest": data["name"]}]


__all__ = ["_jupyter_labextension_paths", "__version__"]
