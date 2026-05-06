# Alarm control panel

**Implementation:** [`alarm_control_panel.py`](../../../custom_components/my_verisure/alarm_control_panel.py)  
**Friendly name:** `ENTITY_NAMES["alarm_control_panel"]` → **My Verisure**  
**Unique ID:** static `"my_verisure"`  

## Supported features

`ARM_AWAY | ARM_HOME | ARM_NIGHT` (`AlarmControlPanelEntityFeature`).

## Codes

`code_format=None`; arm/disarm **without** HA alarm code UI — vendor validates remotely.

## States

Uses `AlarmControlPanelState` values:

- Derived primary state from nested booleans in API payload (`internal.day/night/total`, `external.status`).  
- May expose transitional states for UX (**arming** / **disarming**) via transition helpers — inspect runtime behavior in code (`_transition_state`).

## Attributes

Include parsed booleans and human-readable `active_alarms` list members (`Internal Total`, `Internal Day`, …) — exact keys mirror `_analyze_alarm_states` output.

## Related services

Standard HA services apply (`alarm_control_panel.alarm_arm_*`, `alarm_disarm`) in addition to integration-specific [`my_verisure.*`](../README.md#services) services.
