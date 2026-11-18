# 龙泉水务 (Longquan Water)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Home Assistant 自定义集成，用于监控龙泉水务（天长）有限公司的用水数据。

## 功能特性

- ✅ 支持 UI 配置（config_flow）
- ✅ 实时监控用水数据
- ✅ 查看账户余额和欠费信息
- ✅ 查看水表读数
- ✅ 查看历史用水记录
- ✅ 可配置的扫描间隔（默认 12 小时）

## 安装

### 通过 HACS 安装（推荐）

1. 在 HACS 中点击右上角的三个点
2. 选择 **"自定义仓库"**
3. 添加此仓库的 URL：`https://github.com/zxs1216/longquan_water`
4. 类别选择 **"Integration"**
5. 点击"添加"
6. 在 HACS 中搜索"龙泉水务"并安装
7. 重启 Home Assistant

### 手动安装

1. 下载此仓库
2. 将 `custom_components/longquan_water` 复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹
3. 重启 Home Assistant

## 配置

1. 在 Home Assistant 中，前往 **"配置"** → **"设备与服务"**
2. 点击右下角的 **"+ 添加集成"**
3. 搜索 **"龙泉水务"**
4. 按照提示输入账号信息
   - 客户编号（例如：0101093824）
   - 密码（如有）

## 传感器

此集成会创建以下 11 个传感器：

| 传感器 | 说明 | 单位 |
|--------|------|------|
| `sensor.long_quan_shui_wu_monetary_balance` | 水费卡片数据（包含完整历史数据） | CNY |
| `sensor.long_quan_shui_wu_zhang_hu_yu_e` | 账户余额 | CNY |
| `sensor.long_quan_shui_wu_qian_fei_jin_e` | 欠费金额 | CNY |
| `sensor.long_quan_shui_wu_ying_jiao_jin_e` | 应缴金额 | CNY |
| `sensor.long_quan_shui_wu_shui_biao_du_shu` | 水表读数 | m³ |
| `sensor.long_quan_shui_wu_zui_xin_yong_shui_liang` | 最新用水量 | m³ |
| `sensor.long_quan_shui_wu_zui_xin_shui_fei` | 最新水费 | CNY |
| `sensor.long_quan_shui_wu_zui_jin_12ge_yue_yong_shui_liang` | 最近12个月用水量 | m³ |
| `sensor.long_quan_shui_wu_zui_jin_jiao_fei_jin_e` | 最近缴费金额 | CNY |
| `sensor.long_quan_shui_wu_zui_jin_yi_ci_yong_shui_zhou_qi` | 最近一次用水周期 | - |
| `sensor.long_quan_shui_wu_shua_xin_shi_jian` | 刷新时间 | - |

## 数据属性

每个传感器都包含丰富的额外属性，例如：

- **水费卡片数据传感器** 包含：
  - `daylist` - 每日用水详细记录
  - `monthlist` - 每月用水统计
  - `yearlist` - 每年用水统计
  
- **账户余额传感器** 包含：
  - 客户名称、客户编号
  - 公司名称、用水性质
  - 账户状态、抄表周期
  - 价格、地址

- **水表读数传感器** 包含：
  - 本期用水量、本期水费
  - 本期表底、上期表底
  - 是否已缴费
  - 历史抄表记录

## 数据来源

数据来自：`apiwt.lqswtc.com`

## 选项配置

安装后可以在集成的 **"选项"** 中配置：

- **扫描间隔**（小时）：数据更新频率，默认 12 小时

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

感谢龙泉水务（天长）有限公司提供的数据接口。
