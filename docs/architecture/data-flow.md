# Data flow

## Polling cycle

1. HA scheduler invokes coordinator `_async_update_data`.  
2. `async_login()` validates/refreshes session.  
3. `AlarmUseCase.get_alarm_status` retrieves structured alarm JSON → mapped into coordinator `data["alarm_status"]`.  
4. `InstallationUseCase.get_installation_services` fills `data["detailed_installation"]`.  
5. Entities read coordinator dict on update callbacks.

## Command path (service / UI)

1. UI or service calls coordinator `async_arm_*` / `async_disarm`.  
2. `AlarmUseCase` executes mutation via repository/client.  
3. Coordinator refreshes data + pushes notifications.

## Persistence side channel

`file_manager.save_json(COORDINATOR_DATA_FILE)` duplicates latest coordinator payload for offline/debug resilience — see `load_alarm_info()` helpers.
