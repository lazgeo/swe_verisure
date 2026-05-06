# Troubleshooting

## Enable debug logging

```yaml
logger:
  logs:
    custom_components.my_verisure: debug
```

Reload YAML / restart as needed, reproduce the issue, then download **Home Assistant Core** logs.

## Authentication failures

| Symptom | Things to check |
|---------|-------------------|
| Config flow “invalid auth” | Credentials match the **official app**; account not locked |
| OTP loop | Phone selected receives SMS; OTP entered before expiry |
| Reauth shows `otp_required` | Known limitation: reauth step does not walk OTP flow (`config_flow.py`) — you may need to remove/re-add or fix credentials outside HA |

Session files live under the HA config directory (see coordinator session path pattern).

## Connection / GraphQL errors

- **DNS / firewall** blocking `customers.securitasdirect.es`  
- **TLS interception** on corporate networks  
- **`MyVerisureConnectionError`** — transient network; coordinator raises `UpdateFailed`  

## Service blocked

`MyVerisureServiceBlockedError` shows a **persistent notification** (“service blocked”) — often vendor-side throttling or anti-abuse. Reduce polling frequency in **Options**, avoid rapid repeated service calls.

## Missing or stale entities

- Confirm the config entry is loaded (**Integrations** page).  
- Check **last_updated** sensor if present.  
- Call **`my_verisure.get_status`** once manually.

## Camera images empty

Cameras read **latest files from disk** under the integration’s data layout. If directories are missing, run **Refresh Camera Images** or the **`refresh_camera_images`** service. Check logs from `camera.py` for path errors.

## Collecting a useful bug report

1. HA Core version, integration version (`manifest.json`).  
2. Redacted installation ID.  
3. Log excerpt — include lines containing `my_verisure` and any traceback.  
