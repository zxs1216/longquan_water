# 龙泉水务 (Longquan Water)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Home Assistant 自定义集成，用于监控龙泉水务数据。

## 安装

### 通过 HACS 安装（推荐）

1. 在 HACS 中点击右上角的三个点
2. 选择"自定义仓库"
3. 添加此仓库的 URL：`https://github.com/yourusername/longquan_water`
4. 类别选择 "Integration"
5. 点击"添加"
6. 在 HACS 中搜索"龙泉水务"并安装

### 手动安装

1. 下载此仓库
2. 将 `custom_components/longquan_water` 复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹
3. 重启 Home Assistant

## 配置

1. 在 Home Assistant 中，前往"配置" -> "设备与服务"
2. 点击右下角的"+ 添加集成"
3. 搜索"龙泉水务"
4. 按照提示输入账号信息

## 功能

- 监控用水量
- 查看账户余额
- 可配置的扫描间隔（默认 12 小时）

## 传感器

此集成会创建以下传感器：

- `sensor.longquan_water_<账号>_water_usage` - 用水量
- `sensor.longquan_water_<账号>_water_balance` - 账户余额

## 许可证

MIT License
