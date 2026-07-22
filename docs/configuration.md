# Configuration

## Initial setup

Install Swe Verisure through HACS or copy `custom_components/swe_verisure` into
the Home Assistant configuration directory. Restart Home Assistant, then open
**Settings > Devices & services > Add integration > Swe Verisure**.

The config flow requests the Verisure account email and password. DNI/NIE is
not used. If Verisure requires multifactor authentication, the flow requests a
six-digit verification code. Accounts with several installations get an
installation selector; each selected installation is a separate config entry.

Credentials are stored by Home Assistant in the config entry. They are not read
from `secrets.yaml` by the integration itself. Never include credentials,
session cookies, MFA codes, or downloaded diagnostics in bug reports.

Do not configure Swe Verisure and Home Assistant's built-in Verisure integration
for the same account. Both would poll the same cloud account and can increase
the chance of rate limiting.

## Integration options

Open **Settings > Devices & services**, select Swe Verisure, and choose
**Configure**.

| Option | Default | Allowed values | Effect |
| --- | ---: | --- | --- |
| Number of digits in PIN code for locks | `4` | Integer | Controls the PIN format shown for smart-lock entities. |
| Polling interval | `60` seconds | `10`-`3600` seconds | Controls dynamic device, alarm, event, and optionally user-tracking updates. |
| Enable user location tracking | Off | On/off | Allows the API query that contains account-user location information. |

Changing an option reloads the config entry. Static metadata such as firmware,
Guardian availability, and SMS charging information refreshes at startup and
then hourly; it does not follow shorter polling intervals.

## User location tracking

Location tracking is double opt-in:

1. Enable **Enable user location tracking** in the integration options.
2. Reload completes automatically and creates `device_tracker` entities.
3. Open the entity list and enable only the individual trackers you want.

Tracker entities are disabled by default. When enabled, they may store the
Verisure location name, timestamp, and device name in Home Assistant's recorder.
Tracking names, locations, contact identifiers, and device identifiers are
redacted from integration diagnostics.

## Reauthentication and transient failures

Invalid or expired credentials start Home Assistant's reauthentication flow.
Network errors and Verisure rate limits are treated as transient failures and
retry later; a rate limit must not be interpreted as an incorrect password.
See [Polling and operations](operations.md) for backoff behavior.
