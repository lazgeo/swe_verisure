# Multiple alarms (combined states)

Securitas systems can expose **several logical alarms** at once (internal day/night/total and perimeter/external). This integration models them as:

- **One alarm control panel** — single HA state chosen by **priority** (see [`alarm_control_panel.py`](../../custom_components/my_verisure/alarm_control_panel.py)): internal total dominates, then night, then day, then perimeter.  
- **Binary sensors** — one flag per zone type.  
- **Text sensors** — **Active Alarms** / **General Alarm Status** describe combinations in plain language.

## Practical automation tips

- Use **binary sensors** when automations must distinguish **perimeter-only** vs **internal total**.  
- Use **Active Alarms** when you want a single string for dashboards or notifications.  
- **Panel State** is tuned for automation helpers — verify its exact strings in **Developer tools** for your installation.

## Relation to older guides

The repository root [`MULTIPLE_ALARMS_GUIDE.md`](../../MULTIPLE_ALARMS_GUIDE.md) contains Spanish-oriented examples and Lovelace snippets; entity IDs there may not match your install — always verify live IDs.

## Limitations

The mapping from API payloads to HA states is implemented in code; if the vendor API adds new modes, the integration may need an update. Capture **debug logs** if states look wrong ([Troubleshooting](troubleshooting.md)).
