"""Diagnostics support for Verisure."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import VerisureDataUpdateCoordinator

TO_REDACT = {
    "date",
    "area",
    "deviceArea",
    "deviceId",
    "deviceLabel",
    "deviceName",
    "eventId",
    "eventTime",
    "initials",
    "currentLocationId",
    "currentLocationName",
    "currentLocationTimestamp",
    "name",
    "time",
    "reportTime",
    "userString",
    "userName",
    "webAccount",
    "xbnContactId",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: VerisureDataUpdateCoordinator = entry.runtime_data
    return async_redact_data(coordinator.data, TO_REDACT)
