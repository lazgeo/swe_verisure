# Sensors

Defined in [`sensor.py`](../../../custom_components/my_verisure/sensor.py).

| Logical ID (`sensor_id`) | Friendly name |
|--------------------------|---------------|
| `alarm_status` | General Alarm Status |
| `active_alarms` | Active Alarms |
| `panel_state` | Panel State |
| `last_updated` | Last Updated |

## Unique IDs

Format `{config_entry.entry_id}_{sensor_id}`.

## General Alarm Status

`native_value` returns English descriptive strings combining internal + perimeter booleans, e.g. `Total Internal Active`, `Perimeter Active`, `Alarm Disarmed`. Attributes expose raw booleans (`internal_*_status`, `external_status`, …).

## Active Alarms

Summarizes simultaneous modes — strings may include counts such as `Multiple (n)` depending on implementation branch — verify live entity.

## Panel State

Designed for automation readability — compare against Developer Tools states after pairing.

## Last Updated

Typically exposes timestamp derived from coordinator refresh (`last_updated` field stored as epoch float in coordinator payload — confirm formatting in entity implementation).
