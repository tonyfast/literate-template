# contributing to {{ cookiecutter.name }}

Most things are run with [doit](https://github.com/pydoit/doit).

```bash
doit
```

```py
def task_binder():
    return dict(
        actions=[lambda: print("OK")]
    )
```
