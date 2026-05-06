# Testing strategy

## Current

- **Unit tests** dominate (`pytest`) with mocks/fakes around repositories & use cases.  
- CLI tests validate auxiliary tooling (`cli/tests`).  

## Recommended additions

1. **Contract tests** — snapshot recorded GraphQL responses (sanitized) to detect upstream drift.  
2. **HA integration tests** — minimal harness spinning coordinator + entities using `homeassistant.helpers` test utilities.  
3. **Coverage gates** in CI — enforce thresholds per package.

See also [developer testing](../developer-guide/testing.md).
