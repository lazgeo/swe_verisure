# Auth flow – manual integration checks

This document lists **manual** scenarios to validate the My Verisure authentication and session refresh flow after changes to `SessionManager`, `MyVerisureDataUpdateCoordinator`, and `integration.async_setup_entry`.

## Preconditions

- Home Assistant with `my_verisure` installed from this repo.
- Optional: set logger to `DEBUG` for `custom_components.my_verisure` to see `AUTH_FLOW[...]` lines.

## Test 1 – Token / polling (normal cycle)

1. Start the integration with a valid session.
2. Wait at least one coordinator poll interval (e.g. 10 minutes).
3. **Expect:** Successful update without repeated login storms.
4. **Logs:** `Session refreshed successfully` or `Using existing valid session` (debug); avoid repeated `Service temporarily blocked` during steady state.

## Test 2 – Service blocked during setup

1. Trigger HTTP 403 / rate limit (e.g. many reloads) so `record_service_blocked` / cooldown applies.
2. Restart HA or reload the integration while `coordinator_data.json` still has a snapshot.
3. **Expect:** Entry may start using cached coordinator data; entities show last known state.
4. **Logs:** `Service blocked but using cached data` or `Login failed but using cached data`.

## Test 3 – Options reload with expired session

1. Let the session age past local validity (or shorten only in a dev build), or clear tokens in `~/.my_verisure/session.json` while keeping HA config credentials.
2. Change an integration option (e.g. scan interval) to force `async_reload`.
3. **Expect:** Reload completes; either fresh login or cache fallback without endless `ConfigEntryNotReady` retries hammering login.

## Test 4 – First install (no cache)

1. Remove `~/.my_verisure/session.json` and integration cache under `custom_components/my_verisure/data/` (including `coordinator_data.json` if present).
2. Add the integration and complete the config flow.
3. **Expect:** Successful login; cache files recreated.

## Test 5 – Blocked during normal operation

1. Run the integration until stable.
2. Induce a 403 / “too many requests” once (e.g. repeated reloads).
3. **Expect:** Persistent notification for blocked service; next poll uses cache if available; after cooldown, login resumes without manual intervention.

## Recording results

Use a dated table:

| Date       | Test | Result | Notes |
| ---------- | ---- | ------ | ----- |
| YYYY-MM-DD | 1    | pass   |       |
