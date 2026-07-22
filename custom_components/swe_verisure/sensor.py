"""Support for Verisure sensors."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_GIID, DEVICE_TYPE_NAME, DOMAIN
from .coordinator import VerisureDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Verisure sensors based on a config entry."""
    coordinator: VerisureDataUpdateCoordinator = entry.runtime_data

    sensors: list[Entity] = [VerisureRemainingSms(coordinator)]

    sensors.extend(
        VerisureThermometer(coordinator, serial_number)
        for serial_number, values in coordinator.data["climate"].items()
        if "temperatureValue" in values
    )

    sensors.extend(
        VerisureHygrometer(coordinator, serial_number)
        for serial_number, values in coordinator.data["climate"].items()
        if values.get("humidityEnabled")
    )

    async_add_entities(sensors)


class VerisureThermometer(
    CoordinatorEntity[VerisureDataUpdateCoordinator], SensorEntity
):
    """Representation of a Verisure thermometer."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, coordinator: VerisureDataUpdateCoordinator, serial_number: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{serial_number}_temperature"
        self.serial_number = serial_number

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        device_type = self.coordinator.data["climate"][self.serial_number]["device"][
            "gui"
        ]["label"]
        area = self.coordinator.data["climate"][self.serial_number]["device"]["area"]
        return DeviceInfo(
            name=area,
            manufacturer="Verisure",
            model=DEVICE_TYPE_NAME.get(device_type, device_type),
            identifiers={(DOMAIN, self.serial_number)},
            via_device=(DOMAIN, self.coordinator.config_entry.data[CONF_GIID]),
            configuration_url="https://mypages.verisure.com",
        )

    @property
    def native_value(self) -> str | None:
        """Return the state of the entity."""
        return self.coordinator.data["climate"][self.serial_number]["temperatureValue"]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.serial_number in self.coordinator.data["climate"]
            and "temperatureValue"
            in self.coordinator.data["climate"][self.serial_number]
        )


class VerisureHygrometer(
    CoordinatorEntity[VerisureDataUpdateCoordinator], SensorEntity
):
    """Representation of a Verisure hygrometer."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, coordinator: VerisureDataUpdateCoordinator, serial_number: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{serial_number}_humidity"
        self.serial_number = serial_number

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        device_type = self.coordinator.data["climate"][self.serial_number]["device"][
            "gui"
        ]["label"]
        area = self.coordinator.data["climate"][self.serial_number]["device"]["area"]
        return DeviceInfo(
            name=area,
            manufacturer="Verisure",
            model=DEVICE_TYPE_NAME.get(device_type, device_type),
            identifiers={(DOMAIN, self.serial_number)},
            via_device=(DOMAIN, self.coordinator.config_entry.data[CONF_GIID]),
            configuration_url="https://mypages.verisure.com",
        )

    @property
    def native_value(self) -> str | None:
        """Return the state of the entity."""
        return self.coordinator.data["climate"][self.serial_number]["humidityValue"]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.serial_number in self.coordinator.data["climate"]
            and "humidityValue" in self.coordinator.data["climate"][self.serial_number]
        )


class VerisureRemainingSms(
    CoordinatorEntity[VerisureDataUpdateCoordinator], SensorEntity
):
    """Representation of the installation's remaining SMS balance."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_icon = "mdi:message-text-outline"
    _attr_native_unit_of_measurement = "SMS"
    _attr_translation_key = "remaining_sms"

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this entity."""
        return f"{self.coordinator.config_entry.data[CONF_GIID]}_remaining_sms"

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

    @property
    def native_value(self) -> int | None:
        """Return the remaining SMS count."""
        value = self.coordinator.data.get("remaining_sms")
        return value if isinstance(value, int) else None

    @property
    def extra_state_attributes(self) -> dict[str, bool]:
        """Return which operations consume SMS credits."""
        charges = self.coordinator.data.get("sms_charges")
        if not isinstance(charges, dict):
            return {}
        return {
            key: value
            for key, value in charges.items()
            if key != "__typename" and isinstance(value, bool)
        }
