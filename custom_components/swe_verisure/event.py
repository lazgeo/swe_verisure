"""Event entities for Swe Verisure alarm and activity records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.components.event import EventEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_GIID, DOMAIN
from .coordinator import VerisureDataUpdateCoordinator

SECURITY_EVENT_TYPES = [
    "intrusion",
    "fire",
    "sos",
    "water",
    "animal",
    "technical",
    "warning",
]
ACTIVITY_EVENT_TYPES = ["arm", "disarm", "lock", "unlock", "picture"]
MAX_SEEN_EVENT_IDS = 100


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Verisure event entities."""
    async_add_entities(
        [
            VerisureEvent(
                entry.runtime_data,
                data_key="security_events",
                event_types=SECURITY_EVENT_TYPES,
                translation_key="security",
                unique_id_suffix="intrusion_event",
            ),
            VerisureEvent(
                entry.runtime_data,
                data_key="activity_events",
                event_types=ACTIVITY_EVENT_TYPES,
                translation_key="activity",
                unique_id_suffix="activity_event",
            ),
        ]
    )


class VerisureEvent(CoordinatorEntity[VerisureDataUpdateCoordinator], EventEntity):
    """Report new records from a filtered Verisure event log."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: VerisureDataUpdateCoordinator,
        *,
        data_key: str,
        event_types: list[str],
        translation_key: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialize the event entity."""
        super().__init__(coordinator)
        self._attr_unique_id = (
            f"{coordinator.config_entry.data[CONF_GIID]}_{unique_id_suffix}"
        )
        self._attr_event_types = event_types
        self._attr_translation_key = translation_key
        self._data_key = data_key
        self._seen_event_ids: set[str] = set()
        self._initialized = False

    @property
    def device_info(self) -> DeviceInfo:
        """Return the alarm installation device information."""
        return DeviceInfo(
            name="Verisure Alarm",
            manufacturer="Verisure",
            model="VBox",
            identifiers={(DOMAIN, self.coordinator.config_entry.data[CONF_GIID])},
            configuration_url="https://mypages.verisure.com",
        )

    @staticmethod
    def _event_id(event: Mapping[str, Any]) -> str | None:
        """Return a stable identifier for an event."""
        event_id = event.get("eventId")
        return str(event_id) if event_id is not None else None

    @staticmethod
    def _event_attributes(event: Mapping[str, Any]) -> dict[str, Any]:
        """Return useful event attributes without contact names."""
        device = event.get("device")
        if not isinstance(device, Mapping):
            device = {}
        return {
            "event_id": event.get("eventId"),
            "event_time": event.get("eventTime"),
            "event_category": event.get("eventCategory"),
            "verisure_event_type": event.get("eventType"),
            "event_source": event.get("eventSource"),
            "arm_state": event.get("armState"),
            "area": device.get("area") or event.get("gatewayArea"),
            "device_label": device.get("deviceLabel"),
        }

    def _current_events(self) -> list[Mapping[str, Any]]:
        """Return valid records for this event entity."""
        events = self.coordinator.data.get(self._data_key, [])
        return [event for event in events if isinstance(event, Mapping)]

    def _process_events(self) -> None:
        """Emit unseen events in chronological order."""
        events = self._current_events()
        current_ids = {
            event_id
            for event in events
            if (event_id := self._event_id(event)) is not None
        }

        if not self._initialized:
            self._seen_event_ids = current_ids
            self._initialized = True
            return

        new_events = [
            event
            for event in events
            if (event_id := self._event_id(event)) is not None
            and event_id not in self._seen_event_ids
        ]
        for event in sorted(
            new_events, key=lambda item: str(item.get("eventTime", ""))
        ):
            event_type = str(event.get("eventCategory", "")).lower()
            if event_type not in self.event_types:
                continue
            self._trigger_event(event_type, self._event_attributes(event))
            self.async_write_ha_state()

        self._seen_event_ids.update(current_ids)
        if len(self._seen_event_ids) > MAX_SEEN_EVENT_IDS:
            self._seen_event_ids = current_ids

    async def async_added_to_hass(self) -> None:
        """Register the coordinator listener and establish the initial baseline."""
        await super().async_added_to_hass()
        self._process_events()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Process newly fetched events."""
        self._process_events()
        super()._handle_coordinator_update()
