# Code organization

## Integration layer (`custom_components/my_verisure/`)

| Module | Role |
|--------|------|
| [`integration.py`](../../custom_components/my_verisure/integration.py) | `async_setup_entry`, platforms, services registration, options listener |
| [`coordinator.py`](../../custom_components/my_verisure/coordinator.py) | `DataUpdateCoordinator` subclass — polling, auth, alarm actions, translations |
| [`config_flow.py`](../../custom_components/my_verisure/config_flow.py) | Config + options + reauth flows |
| [`services.py`](../../custom_components/my_verisure/services.py) | Domain services |
| [`alarm_control_panel.py`](../../custom_components/my_verisure/alarm_control_panel.py) | Alarm UI entity |
| [`sensor.py`](../../custom_components/my_verisure/sensor.py) | Text sensors |
| [`binary_sensor.py`](../../custom_components/my_verisure/binary_sensor.py) | Zone binary sensors |
| [`camera.py`](../../custom_components/my_verisure/camera.py) | Snapshot cameras |
| [`button.py`](../../custom_components/my_verisure/button.py) | Refresh button |
| [`device.py`](../../custom_components/my_verisure/device.py) | Device registry helper |

## Domain layer (`custom_components/my_verisure/core/`)

| Area | Role |
|------|------|
| `api/` | GraphQL clients (`auth_client`, `alarm_client`, `installation_client`, `camera_client`, `base_client`) |
| `repositories/` | Repository interfaces + implementations wrapping clients |
| `use_cases/` | Application logic (`AuthUseCase`, `AlarmUseCase`, etc.) |
| `dependency_injection/` | Injector module + providers |
| `session_manager.py` | Session lifecycle |
| `file_manager.py` | Persistence helpers (JSON, camera dirs) |

## Constants

[`core/const.py`](../../custom_components/my_verisure/core/const.py) — domain string, defaults, GraphQL URL, entity friendly names.
