# Configuration

My Verisure uses a **Config Flow** (`config_flow.py`). There is no documented YAML configuration for initial setup.

## Config entry data (stored)

Populated during the flow (see [`config_flow.py`](../../custom_components/my_verisure/config_flow.py)):

| Key | Constant | Description |
|-----|----------|-------------|
| User | `CONF_USER` | Account identifier (e.g. DNI/NIE as used in the mobile app) |
| Password | `CONF_PASSWORD` | Account password |
| Installation ID | `CONF_INSTALLATION_ID` | Selected Securitas installation (`numinst`) |
| Scan interval | `CONF_SCAN_INTERVAL` | Initial polling interval in **minutes** (default from `DEFAULT_SCAN_INTERVAL` = **10** in [`core/const.py`](../../custom_components/my_verisure/core/const.py)) |

Phone / OTP steps use `CONF_PHONE_ID` and `CONF_OTP_CODE` during the flow only.

## Authentication flow (summary)

1. **User step** — credentials submitted; `AuthUseCase.login` runs.  
2. **OTP path** — if `MyVerisureOTPError` is raised, the flow may show **phone selection** then **OTP verification** (`verify_otp`).  
3. **Installation step** — installations are listed; user picks one. Entry is created with title `My Verisure - {alias or id}`.  

If login succeeds without OTP, installation selection follows directly.

## Options flow

**Settings → My Verisure → Configure** opens `MyVerisureOptionsFlowHandler`:

| Option | Constant | Purpose |
|--------|----------|---------|
| Scan interval (minutes) | `CONF_SCAN_INTERVAL` | Coordinator `update_interval` ([Coordinator](../developer-guide/coordinator.md)) |
| Auto arm perimeter with internal | `CONF_AUTO_ARM_PERIMETER_WITH_INTERNAL` | Passed to `arm_away` / `arm_night` use cases when enabled |

Options override entry `data` for scan interval (see `update_listener` in [`integration.py`](../../custom_components/my_verisure/integration.py)).

## Session persistence

- Session material is tied to the account; paths use `STORAGE_DIR` / `my_verisure_{user}.json` pattern in [`coordinator.py`](../../custom_components/my_verisure/coordinator.py).  
- Coordinator attempts **refresh** then **new login** if needed (`async_login`, `async_refresh_session`, `_perform_new_login`).  
- **Reauth** flow exists (`async_step_reauth`); OTP during reauth surfaces as `otp_required` error by design in current code.  

For deeper behavior see [Session persistence](../technical/session-persistence.md).

## Service blocked / rate limiting

`MyVerisureServiceBlockedError` triggers a **persistent notification** and failed update (`UpdateFailed`). See [Troubleshooting](troubleshooting.md).
