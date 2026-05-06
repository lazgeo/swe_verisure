# Development setup

## Repository layout (high level)

```
custom_components/my_verisure/   # HA integration + embedded core
cli/                             # Optional CLI tooling
core/                            # Duplicate/shared core (legacy split — verify which tree CI uses)
requirements.txt                 # Dev/test dependencies at repo root
```

The Home Assistant integration imports **`custom_components.my_verisure.core`** (see [`__init__.py`](../../custom_components/my_verisure/__init__.py)).

## Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Use **`setup_development.py`** at repo root if present for automated bootstrap.

## Running tests

See [testing.md](testing.md) and root [`TESTING.md`](../../TESTING.md). Typical commands:

```bash
./run_tests.sh -f        # fast subset (per project scripts)
python run_all_tests.py    # full suite (if configured)
pytest custom_components/my_verisure/core/tests/unit -q
pytest cli/tests -q
```

## Lint / format

Project docs mention **flake8**, **black**, **mypy** — prefer **`pyproject.toml`** / **ruff** if the repo migrates (see `.cursor/rules/python-standards.mdc`).

## Home Assistant development

For live debugging, symlink or mount `custom_components/my_verisure` into a dev HA `config/` directory and enable debug logging.
