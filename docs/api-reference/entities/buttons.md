# Buttons

[`button.py`](../../../custom_components/my_verisure/button.py)

## Refresh Camera Images

**Name:** `Refresh Camera Images`  
**Unique ID:** `verisure_refresh_camera_images_{installation_id}`  

Pressing executes async service call:

```text
domain: my_verisure
service: refresh_camera_images
data:
  installation_id: <installation_id>
```

Guards against concurrent presses via `_is_executing`; coordinator clears state via `clear_button_executing_state()`.
