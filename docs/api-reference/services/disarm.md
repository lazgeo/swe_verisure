# Service `my_verisure.disarm`

**Schema:** `installation_id` required; **`code` not validated** in schema despite legacy README examples.

Implementation optionally reads `call.data.get("code")` but service registration uses `SERVICE_DISARM_SCHEMA` without `code` field — disarm path ignores HA PIN.

Calls `coordinator.async_disarm()`.
