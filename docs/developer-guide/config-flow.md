# Config flow

Implemented in [`config_flow.py`](../../custom_components/my_verisure/config_flow.py).

## Steps

| Step ID | Purpose |
|---------|---------|
| `user` | Collect username/password; attempt login |
| `phone_selection` | Pick OTP destination |
| `otp_verification` | Enter SMS code (`verify_otp`) |
| `installation` | Choose installation from list |
| `reauth` | Update stored credentials |

## Errors

Mapped to `errors["base"]`: `invalid_auth`, `cannot_connect`, `unknown`, OTP-specific strings, `installation_not_found`, etc.

## Options flow (`MyVerisureOptionsFlowHandler`)

Single step `init` with:

- `CONF_SCAN_INTERVAL` (int minutes)  
- `CONF_AUTO_ARM_PERIMETER_WITH_INTERNAL` (bool)

## Observations for contributors

- **Reauth + OTP**: `async_step_reauth` catches `MyVerisureOTPError` and sets `otp_required` rather than continuing OTP steps — users needing OTP must likely re-add integration or extend the flow.  
- Dependencies: `setup_dependencies()` / `get_*_use_case()` pattern — avoid clearing injector prematurely between steps.
