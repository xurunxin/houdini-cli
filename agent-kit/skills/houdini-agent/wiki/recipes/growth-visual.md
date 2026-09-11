# 植物/根系的可控生长可视化原型

ID: `recipe-growth-visual` · Skill: `houdini-simulation` · **recipe-design-not-runtime-tested**

## 输入
FPS、开始帧、子步、速度单位、初始状态、模拟重置范围、时间依赖的外部输入。

## 最小网络意图
`Growth structure/curves → Reveal/deform or state solver → Sweep/leaves → Cache`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
生长顺序、进度、拓扑稳定、时间状态、实例策略

## 执行
1. 先确定这是视觉演示还是生物模拟；演示优先可控进度，不宣称物理/生物真实性。
2. 基于曲线长度/层级控制根茎展开；只有累积影响后续状态时采用Solver。
3. 将叶片实例和渲染细节与主生长结构分开。

## 验收
- 生长顺序、速度和镜头目标一致。
- 连续帧无枝条突然跳出、拓扑闪烁或穿插失控。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../09-time-state.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/vex/growth_accumulation.vfl)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [C-SOLVER · The Solver SOP](https://tokeru.com/cgwiki/The_solver_sop.html)
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html)
- [E-ATTRACTOR · Entagma / SideFX: VEX strange attractors](https://www.sidefx.com/tutorials/vex-in-houdini-strange-attractors/)
