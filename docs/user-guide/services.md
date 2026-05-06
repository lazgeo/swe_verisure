# Services

Services are registered in [`services.py`](../../custom_components/my_verisure/services.py) and described for the UI in [`services.yaml`](../../custom_components/my_verisure/services.yaml).

**Domain:** `my_verisure`

All handlers locate the `MyVerisureDataUpdateCoordinator` for the given `installation_id` by scanning `hass.data[DOMAIN]` for coordinator instances whose `config_entry.data["installation_id"]` matches.

## `my_verisure.arm_away`

**Data:**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `installation_id` | Yes | string | Installation ID (`numinst`) |

Calls `coordinator.async_arm_away()`. May use **auto arm perimeter with internal** from options/data (`CONF_AUTO_ARM_PERIMETER_WITH_INTERNAL`).

## `my_verisure.arm_home`

| Field | Required | Type |
|-------|----------|------|
| `installation_id` | Yes | string |

Calls `coordinator.async_arm_home()`.

## `my_verisure.arm_night`

| Field | Required | Type |
|-------|----------|------|
| `installation_id` | Yes | string |

Calls `coordinator.async_arm_night()` with the same optional perimeter flag as arm_away.

## `my_verisure.disarm`

| Field | Required | Type |
|-------|----------|------|
| `installation_id` | Yes | string |

**Note:** The Python handler reads optional `call.data.get("code")` but the registered **Voluptuous schema** (`SERVICE_DISARM_SCHEMA`) only requires `installation_id`. So **`code` is not part of the validated schema** — disarm is executed via the API without passing an HA “alarm code”. Do not rely on README examples that show `code` unless the schema is updated to match.

## `my_verisure.get_status`

Triggers `coordinator.async_request_refresh()` for the installation (forces an update cycle).

## `my_verisure.refresh_camera_images`

Runs `coordinator.async_refresh_camera_images()` (pulls/refreshes camera images via use case).

## Example (YAML)

```yaml
service: my_verisure.arm_away
data:
  installation_id: "1234567"
```

```yaml
service: my_verisure.get_status
data:
  installation_id: "1234567"
```

## Related

- Per-service pages: [api-reference/services/](../api-reference/services/)
