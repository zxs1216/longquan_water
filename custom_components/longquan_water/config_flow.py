"""配置流程"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

_LOGGER = logging.getLogger(__name__)

DOMAIN = "longquan_water"

class LongquanWaterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """龙泉水务配置流程"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """处理用户步骤"""
        errors = {}

        if user_input is not None:
            # TODO: 验证用户输入
            return self.async_create_entry(
                title=f"龙泉水务 {user_input.get('account', '')}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("account"): str,
                vol.Optional("password"): str,
            }),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> LongquanWaterOptionsFlow:
        """获取选项流程"""
        return LongquanWaterOptionsFlow(config_entry)


class LongquanWaterOptionsFlow(config_entries.OptionsFlow):
    """龙泉水务选项流程"""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """初始化选项流程"""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """管理选项"""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval_hours",
                    default=self.config_entry.options.get("scan_interval_hours", 12),
                ): int,
            }),
        )
