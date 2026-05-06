# Error handling

| Exception | Typical cause | Coordinator mapping |
|-----------|---------------|---------------------|
| `MyVerisureAuthenticationError` | Bad/expired credentials | `ConfigEntryAuthFailed` |
| `MyVerisureConnectionError` | Network/TLS issues | `UpdateFailed` |
| `MyVerisureServiceBlockedError` | Vendor throttling | Persistent notification + `UpdateFailed` |
| Other `MyVerisureError` | API semantic errors | `UpdateFailed` |

Alarm actions trap generic `Exception`, emit localized persistent notifications, return failing `ArmResult`/`DisarmResult` objects.

Services swallow errors after logging — operators rely on logs + HA notifications.
