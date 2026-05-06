# Logging

- Logger namespace: `custom_components.my_verisure` (`LOGGER` in `core/const.py`).  
- Current code frequently uses **`LOGGER.warning`** for informational traces — expect noisy logs at default INFO/WARNING levels.  
- For troubleshooting instruct users to set **debug** ([user troubleshooting](../user-guide/troubleshooting.md)).  

**Recommendation (future):** demote routine traces to `debug` to reduce noise.
