import re
from pathlib import Path

HERE = Path(__file__).parent

_CONTRIB = HERE / "_contributing.py"


blocks = [
    b[1]
    for b in re.findall(
        r"""([\~\`]{3})py(.*?)\1""",
        (Path(__file__).parent / "contributing.md").read_text(),
        flags=re.M | re.S
    )
]

_CONTRIB.write_text("\n\n".join(blocks))

from _contributing import *
