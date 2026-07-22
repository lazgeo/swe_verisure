# Project Session Notes

## 2026-07-22 initial integration

- Created `swe_verisure` as a standalone HACS custom integration for Swedish
  Verisure accounts without DNI/NIE authentication.
- Based the entity platforms on Home Assistant Core's Verisure integration at
  tag `2026.4.1`; API access uses `vsure==2.9.0` and the Swedish Verisure
  GraphQL login/cookie/token flow.
- Added email/password and MFA config flows, multiple installation selection,
  runtime-data coordinator storage, isolated cookie naming, English/Swedish
  translations, diagnostics, and alarm, binary sensor, camera, lock, sensor,
  and switch platforms.
- Credential-safe live verification passed for login, token refresh, and seven
  read-only coordinator queries. State-changing commands were intentionally not
  run against the live alarm.
- Verification passed with five static tests, Ruff, compileall, JSON/YAML
  parsing, and imports against Home Assistant `2026.4.3`.
- Replaced the Spanish upstream fork contents with the standalone Swe Verisure
  HACS layout and GitHub-specific metadata. The cleanup preserves the fork's
  existing history and does not require a force-push.
- Version 0.1.2 resolves optional `vsure` exception types dynamically because
  Home Assistant's built-in Verisure integration can preload its older library
  version; this prevents `Invalid handler specified` during config-flow import.
- Version 0.1.3 uses explicit localized config-flow labels and stores help text
  as step descriptions, avoiding unresolved shared translation keys in custom
  integrations.
- Version 0.2.0 adds GraphQL intrusion event-log polling to the existing batched
  coordinator request, exposes new intrusion records as a Home Assistant event
  entity, and adds a 60-second default polling option adjustable from 10 to
  3600 seconds.
- Version 0.3.0 broadens alarm events to fire, SOS, water, animal, technical,
  and warning categories; adds a separate arm/disarm/lock/unlock/picture
  activity event entity; and exposes Guardian, SMS balance/charges, read-only
  gateway firmware status, and opt-in disabled-by-default user trackers.
- Dynamic data shares the normal batched poll. SMS metadata, firmware, and
  Guardian status refresh hourly. Personal tracking fields are redacted from
  diagnostics.
- Rate-limit exceptions are handled before their generic login-error base
  class, so `AUT_00021` during setup retries instead of starting reauthentication.
