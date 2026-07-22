# Swe Verisure

`Swe Verisure` is a Home Assistant custom integration for Swedish and other
Verisure accounts served by the `automation01.verisure.com` and
`automation02.verisure.com` GraphQL APIs.

It does not use the Spanish Securitas Direct endpoint and does not ask for a
DNI/NIE. Sign-in uses the account email and password. If Verisure requires
multifactor authentication, the config flow requests and validates the
six-digit verification code.

## Features

- Alarm state and arm/disarm controls
- Door and window binary sensors
- Temperature and humidity sensors
- Broadband status
- Smart cameras and image capture
- Smart locks and autolock controls
- Smart plugs
- Multiple Verisure installations
- Automatic cookie refresh and rate-limit backoff
- Intrusion alarm events from the GraphQL event log
- Configurable polling interval (60 seconds by default; 10-3600 seconds)

## Installation

### HACS

1. Open HACS and choose **Custom repositories**.
2. Add `https://github.com/lazgeo/swe_verisure` as an
   **Integration** repository.
3. Download **Swe Verisure** and restart Home Assistant.
4. Add **Swe Verisure** from **Settings → Devices & services**.

### Manual

Copy `custom_components/swe_verisure` into the same path below the Home
Assistant configuration directory and restart Home Assistant.

Do not configure the built-in Verisure integration for the same account at the
same time. Duplicate polling can trigger Verisure rate limits.

## Authentication

The integration uses [`vsure`](https://github.com/persandstrom/python-verisure),
whose login sequence matches the verified .NET flow: HTTP Basic authentication
to `/auth/login`, persisted Verisure session cookies, `/auth/token` refreshes,
and authenticated GraphQL requests.

## Development status

Version `0.2.0` is an initial implementation. Read-only login, token refresh,
installation discovery, and all seven coordinator queries have been tested
against a live Swedish account. State-changing alarm, lock, smart-plug, and
camera commands were not exercised during development to avoid changing the
live system.

This component is derived from Home Assistant's Apache-2.0 licensed Verisure
integration at tag `2026.4.1`. The Spanish
[`my_verisure`](https://github.com/efraespada/my_verisure) integration was used
as an architectural reference; its DNI/NIE authentication and Spanish GraphQL
models are not included.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
