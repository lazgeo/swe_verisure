# Changelog

All notable changes to Swe Verisure are documented here. The project currently
uses Git tags for HACS distribution; a formal GitHub Release will be published
later when the integration is closer to completion.

## Unreleased

### Documentation

- Added configuration and option reference.
- Added entity, event type, attribute, and service reference.
- Added privacy-safe automation examples.
- Documented polling, hourly metadata refresh, rate-limit backoff, privacy,
  verification scope, and unsupported API operations.

## 0.3.0 - 2026-07-22

### Added

- Fire, SOS, water, animal, technical, and warning security events.
- Separate arm, disarm, lock, unlock, and picture activity events.
- Guardian activation and remaining-SMS diagnostics.
- Read-only gateway firmware update entities.
- Opt-in user location tracking with entities disabled by default.
- English and Swedish labels for the new entities and options.

### Changed

- Static SMS, firmware, and Guardian metadata refreshes hourly rather than on
  every dynamic poll.
- Expanded diagnostics redaction for event and tracking fields.
- Rate-limit exceptions are handled before generic login errors, preventing
  `AUT_00021` from incorrectly starting reauthentication.

## 0.2.0 - 2026-07-22

### Added

- Intrusion event-log polling and a Home Assistant event entity.
- Configurable polling interval, defaulting to 60 seconds with a range of 10 to
  3600 seconds.
- Startup event baseline and runtime event-ID deduplication.

## 0.1.3 - 2026-07-22

### Fixed

- Replaced unresolved shared config-flow translation references with explicit
  English and Swedish labels and descriptions.

## 0.1.2 - 2026-07-22

### Fixed

- Completed compatibility handling for an older `verisure` module preloaded by
  Home Assistant's built-in integration.

## 0.1.1 - 2026-07-22

### Fixed

- Prevented config-flow import failure when optional newer `vsure` exception
  classes are absent from a preloaded older library version.

## 0.1.0 - 2026-07-22

### Added

- Standalone `swe_verisure` HACS integration for email/password Swedish
  Verisure authentication without DNI/NIE.
- MFA, multiple-installation selection, isolated session storage, diagnostics,
  and alarm, binary sensor, camera, lock, sensor, and switch platforms.
