# Utilscripts

Utility scripts to help automate some processes and are hopefully useful.
Most scripts should use `uv`. Refer to `uv`'s website for information, but it would suffice to
install `uv` via their quick start instructions and do `uv run {script_folder}/main.py`
with the correct input arguments.

## Ruff Commands

1. Format all files.

```bash
uv run ruff format .
```

2. Lint and auto -fix

```bash
uv run ruff check --fix .
```