# Agent instructions

## Verification

- Before committing, run `uv run --locked --group dev python -m unittest discover -s tests -v` and `pre-commit run --all-files`.

## Python formatting

- `pre-commit run --all-files` runs Ruff's formatter and may change Python files. Review and stage those changes before committing.
- Install the Git hook once with `pre-commit install` so changed files are formatted during commit.
