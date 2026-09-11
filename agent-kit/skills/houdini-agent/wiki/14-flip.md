# FLIP、海洋、白水与液体网格

ID: `flip` · 领域: SOP / DOP · Skill: `houdini-flip`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
先解决流体体积、碰撞和边界，再把粒子变成可信表面。

## 输入契约
物理尺度、初始液体/持续源、容器、碰撞、速度、粒子分离度、表面和白水需求。

## 推荐操作
1. 选择SOP FLIP或DOP工作流并保持一致；按当前minimal setup与输入标签建立container/source/solver链路。
2. 先低粒子密度验证边界、碰撞厚度、源量和体积保持。薄壁、快速变形和不封闭碰撞是优先排查项。
3. 把模拟缓存和Particle Fluid Surface网格化分开；调粒子尺度与网格平滑时用同一段缓存做对照。
4. 大海面不一定需要全域FLIP：先考察海洋表面表示，仅在交互区域增加模拟。白水是附加系统，独立预算与缓存。

## 验收条件
- 体积/粒子数趋势与源、出口相符，不要求无源量变化时仍固定点数。
- 连续帧没有不可接受的漏水、空洞或网格闪烁。
- 模拟缓存、表面缓存、白水版本可追溯。

## 症状 → 优先检查
**液体穿容器**：检查SDF/碰撞精度、壁厚、运动采样与时间步。
**水面抖动**：先区别粒子模拟噪声还是meshing时间不稳定。
**粘性表现失真**：先核对物理尺度和材料设置，不从教程直接复制数值。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`FLIP Container`、`FLIP Source`、`FLIP Solver`、`Particle Fluid Surface`、`Whitewater Solver`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-FLIP · Fluid simulation](https://www.sidefx.com/docs/houdini/fluid/index.html) — index；
- [S-FLIPMIN · Minimal SOP FLIP setup](https://www.sidefx.com/docs/houdini/fluid/sopminimalsetup.html) — article；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
