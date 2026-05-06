# Layers

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Presentation | `alarm_control_panel.py`, `sensor.py`, … | Entity semantics, attributes |
| Application | `coordinator.py`, `services.py` | Orchestration, HA lifecycle |
| Domain | `core/use_cases/` | Vendor-neutral workflows |
| Infrastructure | `core/repositories/`, `core/api/` | GraphQL & persistence |

Strict layering is **aspirational** — some entities parse raw dict shapes directly for speed; refactoring toward DTOs-only would reduce duplication.
