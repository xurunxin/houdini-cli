# 散布、复制、朝向与打包实例

ID: `instancing` · 领域: SOP / LOP · Skill: `houdini-sop`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
用明确的点属性驱动复制，减少实例方向、缩放和内存错误。

## 输入契约
原型的前向轴/原点、目标点位置、稳定 id、N/up 或 orient、缩放策略、原型选择字段。

## 推荐操作
1. 先用一个带方向标记的非对称原型验证轴向。记录原型默认朝向；不要用球体测试方向是否正确。
2. 按实例属性文档确认 orient 与 N/up、transform 的优先关系；完整矩阵与独立旋转缩放不要重复叠加。
3. 先检查 N/up 长度和共线，再求稳定 frame；复杂路径需要连续 frame，单次 dihedral 不保证 roll 连续。
4. 稳定随机使用 id 和固定 seed。实例数大时保留 packed/instance 表示；SOP packed 和 USD PointInstancer 不应视作相同结构。

## 验收条件
- 抽查首中尾实例的轴向、大小、原型编号。
- 重 cook 和帧变化后稳定 id 的实例不无故跳变。
- 内存与实例数量符合预算；提交时说明是否仍为实例。

## 症状 → 优先检查
**所有物体同向**：检查目标点上的 orient 类型是否四元数、写到了哪一层。
**复制到点后变形**：检查 transform 与 pscale/scale 的组合和源对象变换。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Scatter`、`Copy to Points`、`Pack`、`Attribute Randomize`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-COPY · Copy/instance attributes](https://www.sidefx.com/docs/houdini/copy/instanceattrs.html) — article；
- [C-CHEAT · VEX cheat sheet](https://tokeru.com/cgwiki/VexCheatSheet.html) — selected-sections；
- [J-ATTR · John Kunz VEX Attribute Glossary](https://wiki.johnkunz.com/index.php?title=VEX_Attribute_Glossary) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
