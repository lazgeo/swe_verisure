"""Opt-in Verisure user location trackers."""

from __future__ import annotations

from typing import Any

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.components.device_tracker.const import SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_NOT_HOME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import VerisureDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up disabled-by-default user location trackers."""
    coordinator: VerisureDataUpdateCoordinator = entry.runtime_data
    async_add_entities(
        VerisureUserTracker(coordinator, tracking_id)
        for tracking_id in coordinator.data.get("user_trackings", {})
    )


class VerisureUserTracker(
    CoordinatorEntity[VerisureDataUpdateCoordinator], TrackerEntity
):
    """Representation of a Verisure user's reported location."""

    _attr_entity_registry_enabled_default = False
    _attr_source_type = SourceType.GPS

    def __init__(
        self, coordinator: VerisureDataUpdateCoordinator, tracking_id: str
    ) -> None:
        """Initialize the user tracker."""
        super().__init__(coordinator)
        self._tracking_id = tracking_id
        self._attr_unique_id = f"{tracking_id}_user_tracking"
        tracking = self._tracking()
        self._attr_name = (
            tracking.get("name") or tracking.get("initials") or "Verisure user"
        )

    def _tracking(self) -> dict[str, Any]:
        """Return the current tracking record."""
        tracking = self.coordinator.data.get("user_trackings", {}).get(
            self._tracking_id, {}
        )
        return tracking if isinstance(tracking, dict) else {}

    @property
    def location_name(self) -> str | None:
        """Return the current named Verisure location."""
        tracking = self._tracking()
        if tracking.get("status") != "ACTIVE":
            return None
        return tracking.get("currentLocationName") or STATE_NOT_HOME

    @property
    def available(self) -> bool:
        """Return whether this tracking record is currently available."""
        return super().available and bool(self._tracking())

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return non-coordinate tracking details."""
        tracking = self._tracking()
        return {
            "tracking_status": tracking.get("status"),
            "location_timestamp": tracking.get("currentLocationTimestamp"),
            "device_name": tracking.get("deviceName"),
        }
