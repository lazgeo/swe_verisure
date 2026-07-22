"""Support for Swe Verisure devices."""

from __future__ import annotations

from contextlib import suppress
import os

from homeassistant.components.lock import CONF_DEFAULT_CODE, DOMAIN as LOCK_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.storage import STORAGE_DIR

from .const import CONF_LOCK_DEFAULT_CODE, LOGGER
from .coordinator import VerisureDataUpdateCoordinator

type SweVerisureConfigEntry = ConfigEntry[VerisureDataUpdateCoordinator]

PLATFORMS = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.CAMERA,
    Platform.LOCK,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(
    hass: HomeAssistant, entry: SweVerisureConfigEntry
) -> bool:
    """Set up Swe Verisure from a config entry."""
    coordinator = VerisureDataUpdateCoordinator(hass, entry=entry)

    if not await coordinator.async_login():
        raise ConfigEntryNotReady("Could not log in to Swe Verisure")

    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True


async def update_listener(
    hass: HomeAssistant, entry: SweVerisureConfigEntry
) -> None:
    """Handle options updates."""
    entry.runtime_data.async_update_listeners()


async def async_unload_entry(
    hass: HomeAssistant, entry: SweVerisureConfigEntry
) -> bool:
    """Unload a Swe Verisure config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_entry(
    hass: HomeAssistant, entry: SweVerisureConfigEntry
) -> None:
    """Remove the persisted Verisure session cookie with the config entry."""
    cookie_file = hass.config.path(
        STORAGE_DIR, f"swe_verisure_{entry.data[CONF_EMAIL]}"
    )
    with suppress(FileNotFoundError):
        await hass.async_add_executor_job(os.unlink, cookie_file)


async def async_migrate_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Migrate a Swe Verisure config entry."""
    LOGGER.debug("Migrating from version %s", entry.version)

    if entry.version == 1:
        if config_entry_default_code := entry.options.get(CONF_LOCK_DEFAULT_CODE):
            entity_reg = er.async_get(hass)
            entries = er.async_entries_for_config_entry(entity_reg, entry.entry_id)
            for entity in entries:
                if entity.entity_id.startswith("lock"):
                    entity_reg.async_update_entity_options(
                        entity.entity_id,
                        LOCK_DOMAIN,
                        {CONF_DEFAULT_CODE: config_entry_default_code},
                    )
            new_options = entry.options.copy()
            del new_options[CONF_LOCK_DEFAULT_CODE]
            hass.config_entries.async_update_entry(entry, options=new_options)

        hass.config_entries.async_update_entry(entry, version=2)

    LOGGER.debug("Migration to version %s successful", entry.version)
    return True
