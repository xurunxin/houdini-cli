# Volume / VDB / SDF 数据与运算

ID: `volumes` · 领域: SOP / VEX · Skill: `houdini-volumes`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
把体积当作带空间变换的采样字段，而不是“模糊的网格”。

## 输入契约
字段名、标量/向量、fog或level set、体素尺寸、transform、active bounds、是否封闭几何。

## 推荐操作
1. 先看字段类型、名称和空间范围。SDF 符号与窄带用途不同于密度，不能把 density 直接当 surface。
2. 体积布尔前检查体素与transform一致性；必要时对齐重采样。网格转SDF时先处理开放边和薄片碰撞。
3. 用低分辨率验证形状，再评估细节与内存。固定边界下，均匀三维网格体素边长减半约使单元数八倍；稀疏活跃区变化会使实际增量不同。
4. 可视化切片、iso面与数值范围；不要只靠viewport密度滑块判断数据存在。

## 验收条件
- 正确字段、类型、transform及active bounds。
- 目标厚度与关键形状在选择的体素尺寸下可表达。
- 渲染路径能读回导出的 VDB 字段。

## 症状 → 优先检查
**SDF 合并出现裂缝**：检查level set窄带和transform，不简单叠加。
**体积突然吃满内存**：检查是否激活了大范围背景/转dense，先缩小域再恢复。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`VDB from Polygons`、`VDB Resample`、`VDB Combine`、`Convert VDB`、`Volume Wrangle`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [C-VOLUME · Houdini Volumes](https://tokeru.com/cgwiki/HoudiniVolumes.html) — selected-sections；
- [S-PYROLOOK · Pyro workflow/lookdev](https://www.sidefx.com/docs/houdini/pyro/lookdev.html) — article；
- [S-GEO · hou.Geometry](https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
