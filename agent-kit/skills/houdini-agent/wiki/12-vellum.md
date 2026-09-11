# Vellum：布料、绳索、软体与颗粒

ID: `vellum` · 领域: SOP / DOP · Skill: `houdini-vellum`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
联合检查输入拓扑、约束和碰撞，不只增大刚度。

## 输入契约
模拟几何、约束流、碰撞流；边长分布、厚度、质量、pin与目标动画、预期材料。

## 推荐操作
1. 为布面、曲线/绳、体积软体选择对应的约束构造方式。geometry和constraints为不同数据流；核对当前solver的输入标签。
2. 在单位/尺度明确后设置厚度和质量。检查初始自交、pin集合与目标是否跟随预期动画。
3. 低分辨率测试最剧烈动作。时间子步主要改善时间分辨与碰撞步进，约束迭代改善收敛，两者不能简单互换。
4. 先修碰撞体质量和速度采样，再调子步、迭代、刚度；每次改变一组参数，保存对照。最终平滑/细分与模拟分辨率分离。

## 验收条件
- 几何与约束相匹配，pin位置与意图一致。
- 连续帧检查穿透、拉伸、抖动；记录检查帧段与容忍标准。
- 有可回放缓存及低/高质量设置差异。

## 症状 → 优先检查
**高速碰撞穿透**：先查碰撞厚度/初始重叠/变形采样，再增加子步；不要只提高constraint iterations。
**布无限拉长**：检查约束是否存在、pin目标、刚度和收敛。
**绳子像薄布塌下**：确认使用曲线/拉伸弯曲约束，而非照搬cloth设置。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Vellum Configure Cloth`、`Vellum Configure Hair`、`Vellum Constraints`、`Vellum Solver`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-VELLUM · Vellum](https://www.sidefx.com/docs/houdini/vellum/index.html) — index；
- [S-VELLUMSOLVER · Vellum Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/vellumsolver.html) — selected-sections；
- [S-VELLUMTIPS · Vellum tips](https://www.sidefx.com/docs/houdini/vellum/vellumtips.html) — article；
- [C-VELLUM · Houdini Vellum](https://tokeru.com/cgwiki/HoudiniVellum.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
