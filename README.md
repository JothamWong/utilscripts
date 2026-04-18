# Utilscripts

Utility scripts to help automate some processes and are hopefully useful.
Most scripts should use `uv`. Refer to `uv`'s website for information, but it would suffice to
install `uv` via their quick start instructions and do `uv run {script_folder}/main.py`
with the correct input arguments.

This is also an attempt to understand how to better use uv to handle many packages
within the same root directory.

## uv notes

```bash
uv sync
uv sync --extra index-scraper
uv sync --extra all
```

Adding dependencies to just one tool.

```bash
# shared
uv add <pkg>
# optional, group
uv add --optional <group> <pkg>
# dev tooling
uv add --dev ruff
```

Installing each tool

```bash
# Install just the tool XYZ and its deps
uv tool install ".[index-scraper]"
uv tool install ".[tree-summary]"
# Install everything
uv tool install ".[all]"
```

It seems that this just handles the dependencies but still installs the tools into
the bin directory. Using the tool would then crash as the dependencies are not installed.
The alternative is to treat each tool as a separate pyproject.toml
which does not seem ideal.

## Ruff Commands

1. Format all files.

```bash
uv run ruff format .
```

2. Lint and auto -fix

```bash
uv run ruff check --fix .
```