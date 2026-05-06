# Translations

UI strings for notifications and config flows use JSON under [`custom_components/my_verisure/translations/`](../../custom_components/my_verisure/translations/) (and `strings.json`). The coordinator’s `get_translation()` loads `translations/{language}.json` based on `hass.config.language`, falling back to English.

Alarm panel **state labels** can be customized via Home Assistant’s standard translation mechanisms — see the repository [`TRANSLATION_SYSTEM.md`](../../TRANSLATION_SYSTEM.md) for examples.

## Adding a language

1. Copy `translations/en.json` to `translations/<lang>.json`.  
2. Keep key paths identical; translate values only.  
3. Restart Home Assistant.

## Where translations apply

- Persistent notifications from alarm arm/disarm and service blocked errors (`coordinator.py`).  
- Config flow / options strings via `strings.json` / translation files (standard HA pattern).

If a key is missing, `get_translation` may return the raw key path — see logs if messages look like dotted identifiers.
