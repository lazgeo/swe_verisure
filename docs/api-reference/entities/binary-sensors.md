# Binary sensors

[`binary_sensor.py`](../../../custom_components/my_verisure/binary_sensor.py)

| Sensor ID | Friendly name | Meaning |
|-----------|---------------|---------|
| `internal_day` | Internal Day Alarm | Internal day partition armed |
| `internal_night` | Internal Night Alarm | Internal night partition armed |
| `internal_total` | Internal Total Alarm | Full internal armed |
| `external` | External Alarm | Perimeter / external armed |

**Device class:** `BinarySensorDeviceClass.SAFETY`  
**Unique ID:** `{entry_id}_alarm_{sensor_id}`

Each `is_on` reads coordinator alarm payload branch matching ID.
