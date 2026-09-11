# 属性、组与几何数据契约

ID: `attributes` · 领域: SOP / VEX · Skill: `houdini-sop`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
先理解属性归属和语义，再写 Wrangle 或复制几何。

## 输入契约
Geometry Spreadsheet 或 HOM 属性清单；属性 owner、storage、tuple size、含义、空间与有效范围。

## 推荐操作
1. point 是共享位置，vertex 是某个 primitive 对 point 的引用。需要面间不连续的 UV/法线时，先检查是否应在 vertex 上保存。
2. 在流入节点处写数据契约，如 point P/vector、id/int、pscale/float；primitive name/string；不要让两个不同语义复用同一名字。
3. 属性 Promote 明确聚合方式和是否保留原属性；平均值不是通用正确答案。组是选择集合，属性是数据，两者按需求转换。
4. 重拓扑、融合、排序后重查 id、name、UV、N。复制/打包后区分外层 packed 属性和内部几何属性。

## 验收条件
- 必需属性存在且 owner、类型、tuple size 正确。
- 数值范围、空组、UV接缝和名称唯一性按任务检查。
- 用小样本定位后，对发布所需字段做全量验收或明确抽样范围。

## 症状 → 优先检查
**颜色或 UV 断裂/抹平**：查 owner 与 Promote 聚合，不靠反复 Smooth 掩盖。
**随机变化闪烁**：ptnum 随拓扑变化，改用经过验证的稳定 id。
**Wrangle 读到零**：缺属性可能得到默认值；先 has*attrib 检查，不把零视为真实数据。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Attribute Create`、`Attribute Promote`、`Group Expression`、`Attribute Wrangle`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [C-ATTR · Points, vertices and primitives](https://tokeru.com/cgwiki/Points_and_Verts_and_Prims.html) — article；
- [S-GEO · hou.Geometry](https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html) — selected-sections；
- [J-ATTR · John Kunz VEX Attribute Glossary](https://wiki.johnkunz.com/index.php?title=VEX_Attribute_Glossary) — selected-sections；
- [S-VEX · VEX snippets](https://www.sidefx.com/docs/houdini/vex/snippets.html) — article；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
