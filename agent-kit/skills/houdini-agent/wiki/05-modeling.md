# 程序化建模、曲线、拓扑与 UV

ID: `modeling` · 领域: SOP · Skill: `houdini-sop`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
得到可参数化、可复用、符合下游用途的几何，而不只是静帧像样。

## 输入契约
尺寸/单位、轮廓、曲线方向、封闭要求、法线/UV、目标面数、是否需要后续变形或体积碰撞。

## 推荐操作
1. 选简单表示：规则形体用基本体，连续结构用曲线+截面，复杂融合先比较 Boolean 与体积方案。
2. 先建立主要比例和可控参数，再加倒角与细分。按功能命名输出，如 OUT_RENDER、OUT_COLLISION，不按节点顺序猜出口。
3. 曲线扫掠先控制采样和切线/朝向；Boolean 后查细长面、开放边与退化面；只有下游需要时才重拓扑或三角化。
4. UV 展开和打包要与贴图密度、接缝、UDIM/单图约定一致；程序化变化后回测边界参数。

## 验收条件
- 输出非空、尺寸与包围盒符合设计。
- 法线方向、开放边/非流形、UV与材质标识符合交付约定。
- 极小/默认/极大参数下至少各测一例。

## 症状 → 优先检查
**Sweep 扭转**：先检查曲线顺序、局部 frame 与接近共线的 up，不盲目增加面数。
**Boolean 崩坏**：检查共面/退化/微小比例差，尝试预清理或替代表示。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Curve`、`Resample`、`Sweep`、`Boolean`、`PolyBevel`、`Remesh`、`Normal`、`UV Flatten`、`UV Layout`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-MODEL · Modeling](https://www.sidefx.com/docs/houdini/model/index.html) — index；
- [S-BOX · Box SOP](https://www.sidefx.com/docs/houdini/nodes/sop/box.html) — selected-sections；
- [S-XFORM · Transform SOP](https://www.sidefx.com/docs/houdini/nodes/sop/xform.html) — selected-sections；
- [C-ATTR · Points, vertices and primitives](https://tokeru.com/cgwiki/Points_and_Verts_and_Prims.html) — article；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
