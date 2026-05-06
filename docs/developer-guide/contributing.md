# Contributing

See the repository **[CONTRIBUTING.md](../../CONTRIBUTING.md)** for workflow (fork, branch, PR).

Additional expectations for this integration:

1. **Tests** — add or update unit tests under `custom_components/my_verisure/core/tests/unit/` for core logic changes.  
2. **Docs** — update matching files under `docs/` when user-visible behavior changes.  
3. **No secrets** — never commit credentials, tokens, or raw session JSON.  

CI runs **HACS validation** via [`.github/workflows/validate.yml`](../../.github/workflows/validate.yml).
