# Examples

Copy these YAML fragments into `automations.yaml`, the automation editor, or packages.

**Replace** `INSTALLATION_ID` and entity IDs with values from your system (**Developer tools → States**).

**Inventory:** **30** example `.yaml` files (automation, script, Lovelace, template patterns) under this tree.

## Layout

| Directory | Content | Count |
|-----------|---------|------:|
| [automations/](automations/) | Triggers, schedules, notifications, guards | 16 |
| [scripts/](scripts/) | Sequences using `my_verisure` services | 5 |
| [lovelace/](lovelace/) | Card / stack snippets | 5 |
| [templates/](templates/) | Template sensor / binary ideas | 4 |

Notable filenames from the implementation plan: `arm-on-away.yaml`, `disarm-on-arrival.yaml`, `night-mode.yaml`, `notifications.yaml`, `arm-sequence.yaml`, `status-check.yaml`, `alarm-card.yaml`, `status-panel.yaml`, `mobile-view.yaml`, `custom-sensors.yaml`, `helper-templates.yaml`.

## Safety

Test automations in a **non-production** HA first. Arming/disarming affects real hardware.
