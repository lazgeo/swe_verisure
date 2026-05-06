# Proposed improvements

## Reliability

- Align service unload/register symmetry (`refresh_camera_images`).  
- Transition logging noise from **warning → debug** for routine traces.  
- Harden multi-installation **unique_id** strategy.

## UX

- Extend reauth flow to handle OTP properly.  
- Surface actionable repair issues for auth expiry / blocked service.

## Architecture

- Migrate runtime storage to `entry.runtime_data` pattern where feasible.  
- Consolidate duplicate core packages or document a single source of truth.

## Performance

- Honor backoff when `MyVerisureServiceBlockedError` triggers — avoid hammering vendor API.
