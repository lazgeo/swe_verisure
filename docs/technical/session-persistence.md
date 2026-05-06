# Session persistence

Session manager persists secrets needed to rebuild authenticated GraphQL headers without interactive login each poll.

Paths include JSON stored under Home Assistant’s configuration directory — refer to [`coordinator.py`](../../custom_components/my_verisure/coordinator.py) (`STORAGE_DIR`, `my_verisure_{user}.json`).

## Guidance

- Treat stored JSON like credentials — **exclude from public backups** or encrypt backups at rest.  
- Rotating passwords requires updating the integration credentials (reauth / remove & add).
