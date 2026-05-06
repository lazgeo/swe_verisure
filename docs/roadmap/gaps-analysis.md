# Gaps analysis

## Product / UX gaps

- **Reauth + OTP**: Reauthentication flow surfaces `otp_required` instead of guiding OTP — UX gap for accounts forcing OTP periodically.  
- **Alarm panel unique_id**: Fixed string `my_verisure` may collide with multiple config entries.  
- **Root README** examples still show **`code`** for `disarm` service — inconsistent with actual Voluptuous schema.  
- **`async_unload_services`** previously omitted removing `refresh_camera_images` — **fixed** to unregister all domain services on last entry unload (verify when touching `services.py`).

## Technical debt

- Duplicate core trees (`repo root core/` vs embedded `custom_components/.../core/`) — onboarding friction; clarify authoritative package in README/contributing.  
- Mixed translations (`get_translation` manual JSON vs HA translation framework).  
- Coordinator overrides `async_request_refresh` bypassing standard coordinator scheduling semantics — maintenance burden.

## Testing gaps

- No golden fixture tests mirroring **full Home Assistant** entity lifecycle (only isolated unit tests).  
- Coverage claims in README may drift — automate coverage gates.

## Documentation gaps (historical)

Before `docs/` addition: fragmented guides (`TRANSLATION_SYSTEM.md`, `MULTIPLE_ALARMS_GUIDE.md`). Consolidated navigation now lives under `docs/index.md`.
