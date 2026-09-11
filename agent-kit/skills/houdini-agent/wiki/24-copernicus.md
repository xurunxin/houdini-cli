# Copernicus 与旧 COPs：图像和纹理

ID: `copernicus` · 领域: COP · Skill: `houdini-copernicus`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
以明确分辨率、数据类型和颜色解释建立图像计算图。

## 输入契约
图像/几何输入、层/通道、分辨率、像素/世界空间、颜色与数据语义、目标输出格式。

## 推荐操作
1. 确认当前网络是新Copernicus还是旧COP2；CGWiki旧Cops技巧只迁移思路，不照搬节点/参数。
2. 先低分辨率验证mask、通道和alpha/premultiply约定，再扩展复杂组合。几何导入要确认空间和范围。
3. 程序纹理记录seed、tile需求和位深；normal/height/mask与颜色图采用不同数据解释。
4. 保存后读取实际文件，检查通道、位深、alpha、边缘与平铺；屏幕预览经过view transform不等于原像素。

## 验收条件
- 输出尺寸、通道、数据范围、位深/颜色空间符合目标。
- 贴图在目标材质或应用中通过读回测试。
- 没有把旧COP2参数套进新节点。

## 症状 → 优先检查
**合成边缘有黑边**：检查alpha预乘约定和颜色处理。
**导出颜色与视口不同**：查view transform、文件编码与接收端解释。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Copernicus Network`、`SOP Import`、`ROP Image Output`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-COP · Copernicus](https://www.sidefx.com/docs/houdini/copernicus/index.html) — index；
- [C-COPS · Legacy Houdini COPs](https://tokeru.com/cgwiki/HoudiniCops.html) — selected-sections；
- [S-TERRAINCOP · Copernicus heightfields](https://www.sidefx.com/docs/houdini/heightfields_cop/index.html) — index；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
