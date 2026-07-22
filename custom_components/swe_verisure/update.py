"""Firmware update status for Swe Verisure gateways."""

from __future__ import annotations

from typing import Any

from homeassistant.components.update import UpdateDeviceClass, UpdateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_GIID, DOMAIN
from .coordinator import VerisureDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up gateway firmware entities."""
    coordinator: VerisureDataUpdateCoordinator = entry.runtime_data
    firmware = coordinator.data.get("firmware", {})
    gateways = firmware.get("gateways", []) if isinstance(firmware, dict) else []
    async_add_entities(
        VerisureGatewayFirmware(coordinator, str(gateway["deviceLabel"]))
        for gateway in gateways
        if gateway.get("deviceLabel")
    )


class VerisureGatewayFirmware(
    CoordinatorEntity[VerisureDataUpdateCoordinator], UpdateEntity
):
    """Representation of firmware status for a Verisure gateway."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True
    _attr_translation_key = "gateway_firmware"

    def __init__(
        self, coordinator: VerisureDataUpdateCoordinator, device_label: str
    ) -> None:
        """Initialize the firmware entity."""
        super().__init__(coordinator)
        self._device_label = device_label
        self._attr_unique_id = f"{device_label}_firmware"

    def _gateway(self) -> dict[str, Any]:
        """Return current gateway firmware data."""
        firmware = self.coordinator.data.get("firmware", {})
        if not isinstance(firmware, dict):
            return {}
        return next(
            (
                gateway
                for gateway in firmware.get("gateways", [])
                if gateway.get("deviceLabel") == self._device_label
            ),
            {},
        )

    @property
    def installed_version(self) -> str | None:
        """Return the running firmware version."""
        version = self._gateway().get("reportedRunningFirmware")
        return str(version) if version is not None else None

    @property
    def latest_version(self) -> str | None:
        """Return the latest known firmware version."""
        firmware = self.coordinator.data.get("firmware", {})
        version = firmware.get("latestFirmware") if isinstance(firmware, dict) else None
        return str(version) if version is not None else None

    @property
    def title(self) -> str:
        """Return the update title."""
        return "Verisure gateway firmware"

    @property
    def device_info(self) -> DeviceInfo:
        """Return gateway device information."""
        return DeviceInfo(
            name=f"Verisure Gateway {self._device_label}",
            manufacturer="Verisure",
            model="Gateway",
            identifiers={(DOMAIN, self._device_label)},
            via_device=(DOMAIN, self.coordinator.config_entry.data[CONF_GIID]),
            configuration_url="https://mypages.verisure.com",
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return firmware rollout details."""
        firmware = self.coordinator.data.get("firmware", {})
        if not isinstance(firmware, dict):
            return {}
        return {
            "gateway_status": self._gateway().get("status"),
            "firmware_status": firmware.get("status"),
            "requested_firmware": firmware.get("requestedFirmware"),
            "upgradeable": firmware.get("upgradeable"),
        }
