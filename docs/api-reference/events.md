# Events

The My Verisure integration does **not** define custom integration events under `my_verisure` in the current codebase.

Automations should use standard Home Assistant triggers:

- **`state`** — entity state changes (alarm panel, sensors, binary sensors)  
- **`time`** — schedules  
- **`homeassistant`** — start/shutdown if needed  

If future releases emit events (e.g. `my_verisure.alarm_command_completed`), this page will list payloads and versions.
