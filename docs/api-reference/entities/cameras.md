# Cameras

[`camera.py`](../../../custom_components/my_verisure/camera.py)

## Behavior

- Entity derives snapshot bytes by scanning latest timestamp-named subdirectory under integration-managed camera folders.  
- **No streaming** features (`supported_features = 0`).  
- Device identifiers use `("verisure", device_code)` — note potential overlap across installations if codes collide.

## Operational notes

If directories missing or parse fails, entity logs warnings and returns empty snapshot — run refresh flows ([refresh_camera_images](../../api-reference/services/refresh-camera-images.md)).
