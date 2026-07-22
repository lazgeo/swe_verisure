# Polling, privacy, testing, and limitations

## Polling model

Swe Verisure uses cloud polling; the API does not expose a verified push or
subscription mechanism through `vsure`.

The normal coordinator poll uses one HTTP GraphQL batch containing device
state plus separate security and activity event-log queries. With user tracking
disabled, the dynamic batch contains nine operations. Enabling tracking adds
one operation. SMS metadata, firmware, Guardian status, and remaining SMS add
four operations at startup and on an hourly refresh.

The default interval is 60 seconds and can be configured from 10 to 3600
seconds. Expected event-detection latency is approximately zero to one polling
interval, plus any Verisure event-log ingestion delay.

## Rate limiting

Verisure does not publish a numeric quota for these endpoints. Observed/library
signals include HTTP 429 and codes such as `AUT_00021` and `ACC_00002`.

Coordinator rate limits use increasing retry delays of 5, 15, 30, and 60
minutes. A successful update resets the backoff. Authentication rate limits are
treated as transient; they must not start a false invalid-password flow.

Recommendations:

- Keep the default 60-second interval unless faster detection is necessary.
- Do not run the built-in Verisure integration for the same account.
- Avoid repeated restarts, setup attempts, or MFA requests in a short period.
- Increase the interval if rate limits recur.

## Privacy and diagnostics

User tracking is off by default and its entities are disabled by default.
Enabling trackers can place user names, named locations, timestamps, and device
names in Home Assistant's state history.

Integration diagnostics redact contact and user names, event/device IDs, device
labels/names, areas, event/report times, location IDs/names/timestamps, account
identifiers, and tracking contact IDs. Diagnostics should still be reviewed
before sharing because device capabilities and non-identifying state may remain.

## Intentionally unsupported or redundant API methods

| API capability | Status and reason |
| --- | --- |
| Smart-button configuration/execution | Configuration can be read, but `vsure` has no documented execution mutation. No speculative mutation is sent. |
| Guardian SOS mutation | Not exposed because it can initiate an emergency action and cannot be safely live-tested. |
| Capability and permission metadata | Internal/diagnostic metadata with no useful Home Assistant entity behavior. |
| Alternative latest-camera-image query | Existing image-series and capture paths already provide camera functionality. |
| Per-device smart-plug query | Redundant with the batched smart-plug query. |
| Firmware installation | Firmware status is read-only; Verisure controls installation. |
| Push events | No verified subscription endpoint is available, so event detection is polling-based. |

## Verification status

Read-only authentication, token refresh, installation discovery, expanded
GraphQL batches, metadata shapes, event deduplication, entity registration, and
normal scheduled polling have been verified against a Swedish account without
printing or committing account values.

State-changing alarm, lock, smart-plug, camera, and emergency operations have
not been exercised against the live installation. The integration retains the
control implementations inherited from Home Assistant's Verisure integration,
but cloud/physical completion remains dependent on the installation.
