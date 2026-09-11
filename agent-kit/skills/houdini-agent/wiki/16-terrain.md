# 地形、侵蚀、遮罩与散布

ID: `terrain` · 领域: SOP / COP · Skill: `houdini-terrain`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
把地形、遮罩和散布作为同一坐标系统管理。

## 输入契约
覆盖范围/米制尺度、分辨率、种子、坡度、侵蚀时间、输入DEM数据及坐标参考。

## 推荐操作
1. 确定使用传统SOP HeightField还是新Copernicus地形路径；两条路线的数据域、节点和转换不应混接。
2. 先确定地貌大形、水平/垂直尺度，再加侵蚀和细节。命名height、mask及各类遮罩，确认层实际存在。
3. 在低分辨率验证坡度/沉积等遮罩对植被、岩石和道路的控制；散布原型尺度与地形单位一致。
4. 来自GIS时保存来源/坐标转换与裁剪范围；面向UE/Engine导出时验收高度范围、瓦片接缝、坐标和层名。

## 验收条件
- 尺寸、高度范围、层名及mask范围明确。
- 极值位置、边缘拼接、散布密度与镜头意图一致。
- 导出后在接收端检查，不能只以Houdini视口为准。

## 症状 → 优先检查
**地形太尖或比例怪**：先检查水平/垂直尺度与高度值转换。
**遮罩不生效**：检查同名字段、mask方向与后续节点覆盖。

## 版本与边界
Houdini 22在线文档列出Copernicus heightfields；不等于旧安装自动具备。Entagma H22页面仅作为学习线索。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`HeightField`、`HeightField Noise`、`HeightField Erode`、`HeightField Mask by Feature`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-TERRAIN · Heightfields SOP](https://www.sidefx.com/docs/houdini/heightfields/index.html) — index；
- [S-TERRAINCOP · Copernicus heightfields](https://www.sidefx.com/docs/houdini/heightfields_cop/index.html) — index；
- [E-TERRAIN · Entagma: Heightfields on 3D Objects / Houdini 22](https://entagma.com/heightfields-on-3d-objects-modding-houdini-22/) — landing-only；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
