# Testing

## Suites

| Area | Location | Notes |
|------|----------|-------|
| CLI | [`cli/tests/`](../../cli/tests/) | Commands, helpers, session |
| Embedded core | [`custom_components/my_verisure/core/tests/unit/`](../../custom_components/my_verisure/core/tests/unit/) | Repositories, use cases, DTOs, session manager |

Tests are **pytest**-based. Counts vary over time; the README historically cited ~200+ tests — run `pytest --collect-only` for current numbers.

## Useful commands

```bash
pytest custom_components/my_verisure/core/tests/unit -v
pytest cli/tests -v
```

Coverage scripts (`run_coverage.py`, `run_all_tests.py`) live at repo root.

## Gaps

- Limited **Home Assistant core** integration tests (no `tests/components/my_verisure` style harness in this repo).  
- End-to-end tests depend on **mocked** HTTP — see repository coverage reports for hotspots.

See [testing-strategy.md](../technical/testing-strategy.md) and [roadmap](../roadmap/gaps-analysis.md).
