# Entities

Entities are created **per config entry** (one installation per entry). Platform setup is in [`integration.py`](../../custom_components/my_verisure/integration.py).

Friendly names come from `ENTITY_NAMES` in [`core/const.py`](../../custom_components/my_verisure/core/const.py).

## Naming and IDs

| Platform | Naming | `unique_id` pattern (typical) |
|----------|--------|--------------------------------|
| Alarm control panel | `ENTITY_NAMES["alarm_control_panel"]` → **"My Verisure"** | **`my_verisure`** (fixed string) |
| Sensors | Per-sensor friendly name | `{entry_id}_{sensor_id}` e.g. `{entry}_alarm_status` |
| Binary sensors | Per-sensor friendly name | `{entry_id}_alarm_{sensor_id}` |
| Cameras | `Verisure {device name}` | `verisure_camera_{code}` |
| Button | `Refresh Camera Images` | `verisure_refresh_camera_images_{installation_id}` |

**Important:** The alarm panel uses a **fixed** `unique_id` (`my_verisure`). If you run **multiple config entries**, verify in your HA version whether unique IDs collide; you may need separate HA instances or code changes if collisions occur.

Entity IDs in the UI will look like `alarm_control_panel.my_verisure`, `sensor.<slug>`, etc., depending on HA’s slug rules.

## Alarm control panel

**Class:** `MyVerisureAlarmControlPanel` in [`alarm_control_panel.py`](../../custom_components/my_verisure/alarm_control_panel.py).

**Features:** ARM_AWAY, ARM_HOME, ARM_NIGHT (`AlarmControlPanelEntityFeature`).  
**Codes:** `code_arm_required` and `code_disarm_required` are **False** in code — disarm does not use an HA alarm code (Securitas validates on API side).

**State mapping (summary):** Primary HA state is derived from internal day/night/total and external flags with priority **Total → Night → Day → External → Disarmed**. Transition states **arming** / **disarming** may be shown for UX during operations.

See [alarm-control-panel.md](../api-reference/entities/alarm-control-panel.md) for attributes and behavior details.

## Sensors

All in [`sensor.py`](../../custom_components/my_verisure/sensor.py):

| Purpose | `sensor_id` | Friendly name (const) |
|---------|---------------|------------------------|
| Aggregate text status | `alarm_status` | General Alarm Status |
| Human-readable active modes | `active_alarms` | Active Alarms |
| Automation-friendly panel state | `panel_state` | Panel State |
| Last coordinator refresh | `last_updated` | Last Updated |

**Alarm status** strings include values such as `Total Internal Active`, `Internal Day Active`, `Perimeter Active`, `Alarm Disarmed`, etc., based on internal/external booleans (English strings in code).

## Binary sensors

Device class **SAFETY**. Types: **internal_day**, **internal_night**, **internal_total**, **external** — each reflects the corresponding flag in coordinator alarm payload.

## Cameras

[`camera.py`](../../custom_components/my_verisure/camera.py): images are read from on-disk paths under the integration file manager (`cameras/{type}{code}/timestamp dirs`). No RTSP/stream — **still image** from latest captured file.

## Buttons

**Refresh Camera Images** triggers the domain service `my_verisure.refresh_camera_images` for the installation ([Services](services.md)).

## Device registry

[`device.py`](../../custom_components/my_verisure/device.py) supplies device info (manufacturer Verisure, model Alarm System, etc.).
