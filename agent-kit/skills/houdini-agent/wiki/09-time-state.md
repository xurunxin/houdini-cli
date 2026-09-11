# 时间、反馈、模拟选择与重算

ID: `time-state` · 领域: SOP / DOP / CHOP · Skill: `houdini-simulation`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
把按帧求值、时间采样、积分状态和缓存回放分开。

## 输入契约
FPS、开始帧、子步、速度单位、初始状态、模拟重置范围、时间依赖的外部输入。

## 推荐操作
1. 先问效果是 f(input,t) 还是必须依赖上一状态；噪声动画不一定需要模拟，生长累积通常需要显式状态。
2. 反馈网络标明 previous state 和 current input；初始化与逐步更新分开，避免把初始源每帧重复累加。
3. 改变初始输入/约束/solver参数后按依赖范围失效缓存；从开始帧顺序模拟，不把任意跳帧当可靠积分。
4. 按现象选求解器：刚性碎片→RBD；布/绳/软约束→Vellum；烟火→Pyro；自由液面→FLIP；材料连续体→考察 MPM。

## 验收条件
- 记录模拟起点、FPS、子步和缓存版本。
- 连续帧上无无意的重置、速度突变或缺帧。
- 同一来源可区分重新模拟与缓存播放。

## 症状 → 优先检查
**中间帧状态不对**：检查是否依赖之前帧但未运行或缓存丢失。
**运动快慢异常**：检查每帧量与每秒量、FPS、TimeInc及输入重定时。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Solver SOP`、`DOP Network`、`Time Shift`、`Time Blend`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [C-SOLVER · The Solver SOP](https://tokeru.com/cgwiki/The_solver_sop.html) — article；
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html) — index；
- [E-ATTRACTOR · Entagma / SideFX: VEX strange attractors](https://www.sidefx.com/tutorials/vex-in-houdini-strange-attractors/) — landing-only；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
