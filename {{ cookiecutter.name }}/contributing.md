# contributing to {{ cookiecutter.name }}

Most things are run with [doit](https://github.com/pydoit/doit).

```bash
doit
```

## Prerequisites

```py
import json, os, sys, subprocess, toml
from pathlib import Path
```


### doit configuration and environment

```py
from doit.tools import config_changed
from doit.action import CmdAction

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread"
}

os.environ.update(
    PYTHONUNBUFFERED="1",
    PYTHONIOENCODING="utf-8",
    NODE_OPTIONS="--max-old-space-size=4096",
)
```

## Key Paths

```py
HERE = Path(__file__).parent.resolve()
BUILD = HERE / "build"
BUILD.exists() or BUILD.mkdir()
PYPROJECT_TOML = HERE / "pyproject.toml"
SETUP_PY = HERE / "setup.py"
PYPROJECT = toml.loads(PYPROJECT_TOML.read_text())
FLIT = PYPROJECT["tool"]["flit"]
METADATA = FLIT["metadata"]
PY_NAME = METADATA["module"]
# TODO: decide source of truth
VERSION = "0.1.0"
SRC_PY = HERE / "src" / PY_NAME
JS = SRC_PY / "js"
```

## Goals

### Binder
The software should work on [Binder](https://mybinder.org) in a development-like
state.

```py
INSTALLED_EXTS = BUILD / "jupyter-labextension-list.log"
PIP_FROZEN = BUILD / "pip-freeze.log"

def task_binder():
    return dict(
        actions=[lambda: print("OK FOR BINDER")],
        file_dep=[INSTALLED_EXTS, PIP_FROZEN]
    )
```

### Release

```py

DIST = HERE / "dist"
SDIST = DIST / f"{PY_NAME}-{VERSION}.tar.gz"
WHEEL = DIST / f"{PY_NAME}-{VERSION}-py3-none-any.whl"

def task_release():
    return dict(
        actions=[lambda: print("OK TO RELEASE")],
        targets=[SDIST, WHEEL]
    )
```

## JS

The JavaScript side of the house is handled by `jlpm`.

```py

PACKAGE_JSON = JS / "package.json"
NODE_MODULES = JS / "node_modules"
YARN_LOCK = JS / "yarn.lock"
YARN_INTEGRITY = NODE_MODULES / ".yarn-integrity"

SRC_TS = JS / "src"
ALL_TS = sorted(SRC_TS.rglob("*.ts"))
JS_LIB = JS / "lib"
ALL_JS = [JS_LIB / "index.js", JS_LIB / "plugin.js"]

STATIC_OUT = SRC_PY / "static"
# this contains the name of the `remoteEntry.<hash>.js`
STATIC_PKG_JSON = STATIC_OUT / "package.json"

def task_jlpm():
```

### Install packages

```py
    yield dict(
        name="install",
        file_dep=[PACKAGE_JSON, YARN_LOCK],
        actions=[jlpm(["--prefer-offline", "--ignore-optional"])],
        targets=[YARN_INTEGRITY]
    )
```

### Build Typescript

```py
    yield dict(
        name="tsc",
        file_dep=[YARN_INTEGRITY, *ALL_TS],
        actions=[jlpm(["build:ts"])],
        targets=[*ALL_JS]
    )
```

### Build Lab Extension

```py
    yield dict(
        name="ext",
        file_dep=[*ALL_JS],
        actions=[jlpm(["build:ext"])],
        targets=[STATIC_PKG_JSON]
    )
```

## Development Install

A number of tasks ensure working with the JS and python packages during development.

```py

LABEXT = [sys.executable, "-m", "jupyter", "labextension"]

def task_dev():
    yield dict(
        name="js",
        file_dep=[PIP_FROZEN],
        actions=[
            [*LABEXT, "develop", "--overwrite", "."],
            _log([*LABEXT, "list"], INSTALLED_EXTS),
        ],
        targets=[INSTALLED_EXTS],
    )
```

```py
    yield dict(
        name="py",
        actions=[
            [sys.executable, "-m", "pip", "install", "-e", ".", "--no-deps"],
            _log(["pip", "freeze"], PIP_FROZEN),
        ],
        file_dep=[SETUP_PY, STATIC_PKG_JSON],
        targets=[PIP_FROZEN],
    )

```


## Utilities
```py
def jlpm(args):
    return CmdAction(["jlpm", *args], cwd=JS, shell=False)

def _log(args, path, **kwargs):
    def _run():
        if not path.parent.exists():
            path.parent.mkdir(exist_ok=True)
        path.write_bytes(subprocess.check_output(args, **kwargs))

    return _run
```
