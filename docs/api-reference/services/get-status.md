# Service `my_verisure.get_status`

**Schema:** requires `installation_id`.

Calls `coordinator.async_request_refresh()` (invokes internal update path). Use sparingly to avoid additional API load on top of poll interval.
