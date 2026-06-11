from __future__ import annotations

import asyncio

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LiquidCheckCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: LiquidCheckCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LiquidCheckStartMeasureButton(coordinator, entry)])


class LiquidCheckStartMeasureButton(
    CoordinatorEntity[LiquidCheckCoordinator],
    ButtonEntity,
):
    _refresh_delay_seconds = 10
    _attr_has_entity_name = True
    _attr_entity_registry_enabled_default = True
    _attr_name = "Messung starten"
    _attr_translation_key = "start_measure"
    _attr_icon = "mdi:play-circle-outline"

    def __init__(self, coordinator: LiquidCheckCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        host = entry.data[CONF_HOST]
        self._attr_unique_id = f"{self._get_legacy_serial(host)}_start_measure"
        self._attr_suggested_object_id = "start_measure"

    def _get_legacy_serial(self, host: str) -> str:
        data = self.coordinator.data or {}
        device = data.get("device", {}) if isinstance(data, dict) else {}
        return f"{device.get('uuid') or device.get('serial') or host}{host}"

    @property
    def device_info(self) -> DeviceInfo:
        data = self.coordinator.data or {}
        device = data.get("device", {}) if isinstance(data, dict) else {}
        host = self._entry.data[CONF_HOST]
        serial = self._get_legacy_serial(host)

        return DeviceInfo(
            identifiers={(DOMAIN, serial)},
            name=device.get("name") or self._entry.title,
            manufacturer="SI-Elektronik GmbH",
            model="Liquid-Check",
            sw_version=device.get("firmware"),
            configuration_url=f"http://{host}",
        )

    async def async_press(self) -> None:
        await self.coordinator.api.async_start_measure()
        await asyncio.sleep(self._refresh_delay_seconds)
        await self.coordinator.async_request_refresh()
