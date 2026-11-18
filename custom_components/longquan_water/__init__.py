"""龙泉水务集成"""
from __future__ import annotations

import logging
from datetime import timedelta, datetime

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "longquan_water"
PLATFORMS = [Platform.SENSOR]

API_BASE_URL = "https://apiwt.lqswtc.com"
API_TIMEOUT = 30

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置配置条目"""
    hass.data.setdefault(DOMAIN, {})

    # 获取扫描间隔（小时）
    scan_interval_hours = entry.options.get("scan_interval_hours", 12)

    coordinator = LongquanWaterCoordinator(
        hass,
        entry,
        timedelta(hours=scan_interval_hours),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载配置条目"""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class LongquanWaterCoordinator(DataUpdateCoordinator):
    """龙泉水务数据更新协调器"""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        update_interval: timedelta,
    ) -> None:
        """初始化协调器"""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.entry = entry
        self.session = async_get_clientsession(hass)
        self._token = None

    async def _async_update_data(self) -> dict:
        """获取龙泉水务数据"""
        try:
            # 登录获取 token
            if not self._token:
                await self._async_login()

            # 获取用户信息和用水数据
            async with async_timeout.timeout(API_TIMEOUT):
                user_info = await self._async_get_user_info()
                water_data = await self._async_get_water_data()

            return {
                "user_info": user_info,
                "water_data": water_data,
                "update_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            }

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"连接龙泉水务服务器失败: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"获取数据失败: {err}") from err

    async def _async_login(self) -> None:
        """登录获取访问令牌"""
        account = self.entry.data.get("account")
        password = self.entry.data.get("password", "")

        login_url = f"{API_BASE_URL}/api/login"
        payload = {
            "account": account,
            "password": password,
        }

        async with async_timeout.timeout(API_TIMEOUT):
            response = await self.session.post(login_url, json=payload)
            response.raise_for_status()
            data = await response.json()

            if data.get("code") == 200:
                self._token = data.get("data", {}).get("token")
            else:
                raise UpdateFailed(f"登录失败: {data.get('message', '未知错误')}")

    async def _async_get_user_info(self) -> dict:
        """获取用户信息"""
        url = f"{API_BASE_URL}/api/user/info"
        headers = {"Authorization": f"Bearer {self._token}"}

        async with async_timeout.timeout(API_TIMEOUT):
            response = await self.session.get(url, headers=headers)
            response.raise_for_status()
            data = await response.json()

            if data.get("code") == 200:
                return data.get("data", {})
            else:
                raise UpdateFailed(f"获取用户信息失败: {data.get('message')}")

    async def _async_get_water_data(self) -> dict:
        """获取用水数据"""
        url = f"{API_BASE_URL}/api/water/usage"
        headers = {"Authorization": f"Bearer {self._token}"}

        async with async_timeout.timeout(API_TIMEOUT):
            response = await self.session.get(url, headers=headers)
            response.raise_for_status()
            data = await response.json()

            if data.get("code") == 200:
                return data.get("data", {})
            else:
                raise UpdateFailed(f"获取用水数据失败: {data.get('message')}")
