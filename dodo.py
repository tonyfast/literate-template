from pathlib import Path

HERE = Path(__file__).parent

CC = HERE / "{{ cookiecutter.name }}"

def task_test():
    return dict(
        file_dep=[*CC.rglob("*")],
        actions=[["cookiecutter", ".", "-f", "--no-input"]]
    )
