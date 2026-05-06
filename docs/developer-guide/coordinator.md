# Coordinator

`MyVerisureDataUpdateCoordinator` ([`coordinator.py`](../../custom_components/my_verisure/coordinator.py)) subclasses Home Assistant’s `DataUpdateCoordinator`.

## Update interval

Constructed with `update_interval=timedelta(minutes=scan_interval_minutes)` where `scan_interval_minutes` comes from **options** then **config entry data**, defaulting to `DEFAULT_SCAN_INTERVAL` (**10** minutes).

Changing options triggers `update_listener` in [`integration.py`](../../custom_components/my_verisure/integration.py) which assigns `coordinator.update_interval`.

## `_async_update_data`

1. `async_login()` — uses existing session, refresh, or new login via `AuthUseCase`.  
2. `alarm_use_case.get_alarm_status(installation_id)`  
3. `installation_use_case.get_installation_services(installation_id)`  
4. Builds `result` dict with `alarm_status`, `detailed_installation`, `last_updated`.  
5. Persists JSON via `file_manager.save_json(COORDINATOR_DATA_FILE, ...)`.  
6. Calls dummy camera image bootstrap.

Exceptions:

- `MyVerisureAuthenticationError` → `ConfigEntryAuthFailed`  
- `MyVerisureConnectionError`, generic `MyVerisureError`, others → `UpdateFailed`  
- `MyVerisureServiceBlockedError` → notification + `UpdateFailed`

## Alarm commands

`async_arm_*` / `async_disarm` delegate to `AlarmUseCase`, send persistent notifications via `get_translation`, refresh data on success.

## Registration hooks

`register_alarm_control_panel` / `register_button` allow clearing transitional UI states after service calls.

## Logging

Uses package logger `MyVerisure` / module loggers — expect **warning** level noise in normal operation (`LOGGER.warning` used frequently).
