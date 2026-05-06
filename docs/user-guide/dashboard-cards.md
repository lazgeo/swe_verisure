# Dashboard cards (Lovelace)

## Alarm panel

Use the built-in **Alarm panel** card targeting `alarm_control_panel.my_verisure` (or the entity ID shown in **Developer tools → States**).

```yaml
type: alarm-panel
entity: alarm_control_panel.my_verisure
```

States follow Home Assistant’s alarm panel model (`armed_away`, `armed_home`, `armed_night`, `disarmed`, plus transitional states if shown by the integration).

## Status overview

Use an **Entities** card for:

- `sensor.*active_alarms*` — quick human-readable summary  
- `sensor.*panel_state*` — better for logic/automation-friendly state  
- Binary sensors for each zone  

```yaml
type: entities
title: Verisure
entities:
  - entity: sensor.my_verisure_active_alarms
  - entity: sensor.my_verisure_panel_state
  - entity: binary_sensor.my_verisure_alarm_internal_total
  - entity: binary_sensor.my_verisure_alarm_external
```

Exact entity IDs depend on your config entry; copy from the UI.

## Cameras

Use **Picture entity** or **Picture glance** with camera entities created for your devices. Images are **static snapshots** from disk, not live streams (see [Entities](entities.md)).

## Multiple alarms

See [Multiple alarms](multiple-alarms.md) and [examples](../examples/lovelace/dashboard-status.yaml) for stacked layouts.
