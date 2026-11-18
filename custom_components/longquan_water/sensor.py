"""传感器平台"""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN = "longquan_water"

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置传感器"""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # TODO: 根据实际数据添加传感器
    entities = [
        LongquanWaterSensor(coordinator, entry, "water_usage", "用水量"),
        LongquanWaterSensor(coordinator, entry, "water_balance", "余额"),
    ]

    async_add_entities(entities)


class LongquanWaterSensor(CoordinatorEntity, SensorEntity):
    """龙泉水务传感器"""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
        name: str,
    ) -> None:
        """初始化传感器"""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"{entry.title} {name}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"

    @property
    def native_value(self) -> float | None:
        """返回传感器状态"""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None
