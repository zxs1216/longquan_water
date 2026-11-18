"""传感器平台"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "longquan_water"

# 传感器定义
SENSOR_TYPES = {
    "card_data": {
        "name": "水费卡片数据",
        "icon": "mdi:water",
        "device_class": SensorDeviceClass.MONETARY,
        "unit": "CNY",
    },
    "balance": {
        "name": "账户余额",
        "icon": "mdi:currency-cny",
        "device_class": SensorDeviceClass.MONETARY,
        "unit": "CNY",
    },
    "arrears": {
        "name": "欠费金额",
        "icon": "mdi:alert-circle",
        "device_class": SensorDeviceClass.MONETARY,
        "unit": "CNY",
    },
    "due_amount": {
        "name": "应缴金额",
        "icon": "mdi:cash",
        "device_class": SensorDeviceClass.MONETARY,
        "unit": "CNY",
    },
    "meter_reading": {
        "name": "水表读数",
        "icon": "mdi:water-pump",
        "device_class": SensorDeviceClass.WATER,
        "unit": UnitOfVolume.CUBIC_METERS,
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    "latest_usage": {
        "name": "最新用水量",
        "icon": "mdi:water",
        "device_class": SensorDeviceClass.WATER,
        "unit": UnitOfVolume.CUBIC_METERS,
    },
    "latest_amount": {
        "name": "最新水费",
        "icon": "mdi:cash",
        "device_class": SensorDeviceClass.MONETARY,
        "unit": "CNY",
    },
    "recent_12_month_usage": {
        "name": "最近12个月用水量",
        "icon": "mdi:water",
        "device_class": SensorDeviceClass.WATER,
        "unit": UnitOfVolume.CUBIC_METERS,
    },
    "last_payment_amount": {
        "name": "最近缴费金额",
        "icon": "mdi:cash-check",
        "device_class": SensorDeviceClass.MONETARY,
        "unit": "CNY",
    },
    "latest_usage_date": {
        "name": "最近一次用水周期",
        "icon": "mdi:calendar",
    },
    "update_time": {
        "name": "刷新时间",
        "icon": "mdi:clock-outline",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置传感器"""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        LongquanWaterSensor(coordinator, entry, sensor_type, sensor_config)
        for sensor_type, sensor_config in SENSOR_TYPES.items()
    ]

    async_add_entities(entities)


class LongquanWaterSensor(CoordinatorEntity, SensorEntity):
    """龙泉水务传感器"""

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        sensor_type: str,
        sensor_config: dict,
    ) -> None:
        """初始化传感器"""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"{entry.title.split()[0]} {sensor_config['name']}"
        self._attr_unique_id = f"{entry.unique_id}_{sensor_type}"
        self._attr_icon = sensor_config.get("icon")

        if "device_class" in sensor_config:
            self._attr_device_class = sensor_config["device_class"]
        if "unit" in sensor_config:
            self._attr_native_unit_of_measurement = sensor_config["unit"]
        if "state_class" in sensor_config:
            self._attr_state_class = sensor_config["state_class"]

        # 设置设备信息
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.unique_id)},
            "name": entry.title,
            "manufacturer": "龙泉水务",
            "model": "智能水表",
        }

    @property
    def native_value(self) -> Any:
        """返回传感器状态"""
        if not self.coordinator.data:
            return None

        water_data = self.coordinator.data.get("water_data", {})

        # 根据传感器类型返回对应的值
        if self._sensor_type == "card_data":
            return water_data.get("balance")
        elif self._sensor_type == "balance":
            return water_data.get("balance")
        elif self._sensor_type == "arrears":
            return water_data.get("arrears")
        elif self._sensor_type == "due_amount":
            return water_data.get("due_amount")
        elif self._sensor_type == "meter_reading":
            return water_data.get("meter_reading")
        elif self._sensor_type == "latest_usage":
            return water_data.get("latest_usage")
        elif self._sensor_type == "latest_amount":
            return water_data.get("latest_amount")
        elif self._sensor_type == "recent_12_month_usage":
            return water_data.get("total_usage")
        elif self._sensor_type == "last_payment_amount":
            return water_data.get("last_payment_amount")
        elif self._sensor_type == "latest_usage_date":
            return water_data.get("latest_usage_date")
        elif self._sensor_type == "update_time":
            return self.coordinator.data.get("update_time")

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """返回额外属性"""
        if not self.coordinator.data:
            return {}

        water_data = self.coordinator.data.get("water_data", {})
        user_info = self.coordinator.data.get("user_info", {})

        attrs = {
            "数据来源": "apiwt.lqswtc.com",
        }

        # 水费卡片数据传感器包含完整的历史数据
        if self._sensor_type == "card_data":
            attrs.update({
                "balance": water_data.get("balance"),
                "date": self.coordinator.data.get("update_time"),
                "daylist": water_data.get("daylist", []),
                "monthlist": water_data.get("monthlist", []),
                "yearlist": water_data.get("yearlist", []),
                "utility_type": "water",
                "unit": "m³",
                "total_usage": water_data.get("total_usage"),
                "meter_reading": water_data.get("meter_reading"),
                "recent_12_month_usage": water_data.get("total_usage"),
                "last_payment_amount": water_data.get("last_payment_amount"),
                "latest_usage": water_data.get("latest_usage"),
                "latest_amount": water_data.get("latest_amount"),
                "latest_usage_date": water_data.get("latest_usage_date"),
                "arrears": water_data.get("arrears"),
                "due_amount": water_data.get("due_amount"),
            })

        # 账户余额传感器包含账户信息
        elif self._sensor_type == "balance":
            attrs.update({
                "账户余额_元": water_data.get("balance"),
                "欠费金额_元": water_data.get("arrears"),
                "应缴金额_元": water_data.get("due_amount"),
                "客户名称": user_info.get("customer_name"),
                "客户编号": user_info.get("customer_code"),
                "公司名称": user_info.get("company_name"),
                "用水性质": user_info.get("water_type"),
                "口径": user_info.get("caliber"),
                "账户状态": user_info.get("account_status"),
                "抄表周期": user_info.get("meter_cycle"),
                "价格": user_info.get("price"),
                "地址": user_info.get("address"),
                "更新时间": self.coordinator.data.get("update_time"),
            })

        # 水表读数传感器包含用水历史
        elif self._sensor_type == "meter_reading":
            latest_day = water_data.get("daylist", [{}])[0] if water_data.get("daylist") else {}
            attrs.update({
                "数据周期": water_data.get("latest_usage_date"),
                "本期用水量_m3": latest_day.get("usge"),
                "本期水费_元": latest_day.get("money"),
                "本期表底": latest_day.get("endScale"),
                "上期表底": latest_day.get("beginScale"),
                "是否已缴费": latest_day.get("isPay", False),
                "daylist": water_data.get("daylist", []),
                "总期数": len(water_data.get("daylist", [])),
                "更新时间": self.coordinator.data.get("update_time"),
            })

        return attrs
