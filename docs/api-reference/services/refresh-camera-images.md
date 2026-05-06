# Service `my_verisure.refresh_camera_images`

**Schema:** requires `installation_id`.

Calls `coordinator.async_refresh_camera_images()` which runs the camera refresh use case (retry/interval parameters set in code — see coordinator implementation).

On completion attempts to clear button executing state.
