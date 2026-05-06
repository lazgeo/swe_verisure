# Phase 1 — Short term

**Goals:** Stability, doc/code alignment, minimal risk fixes.

| Task | Impact |
|------|--------|
| ~~Fix service unload parity~~ | Done — `refresh_camera_images` now removed in `async_unload_services` |
| Fix README disarm example vs schema | Removes user confusion |
| Demote noisy logs to debug | Cleaner production logs |
| Add regression tests for services unload/register | Safer refactors |

**Expected outcome:** Fewer support tickets, predictable lifecycle.
