import re
from pathlib import Path

# yep
eval("".join([
    block[2] for block in re.findall(
        r"""([\~\`]{3})py(\n[.\n]*\n)\1""",
        (Path(__file__).parent / "contributing.md").read_text())]))
