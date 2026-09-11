# 诊断布料穿透而不盲目增大刚度

ID: `recipe-cloth-penetration` · Skill: `houdini-vellum` · **recipe-design-not-runtime-tested**

## 输入
模拟几何、约束流、碰撞流；边长分布、厚度、质量、pin与目标动画、预期材料。

## 最小网络意图
`Cloth mesh + constraints + collision → Vellum Solver → Cache`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
厚度、碰撞体、pin、子步、约束迭代、时间采样

## 执行
1. 查看初始自交、cloth/collision尺度、碰撞体质量和pin目标。
2. 用最剧烈动作的短帧段测试；先修碰撞几何/采样，再提高时间子步。
3. 约束迭代针对拉伸收敛单独调；每组改动保存对照缓存。

## 验收
- 报告测试帧段的穿透情况与容忍标准。
- pin不意外脱落，拉伸和运动都符合brief。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../12-vellum.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-VELLUM · Vellum](https://www.sidefx.com/docs/houdini/vellum/index.html)
- [S-VELLUMSOLVER · Vellum Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/vellumsolver.html)
- [S-VELLUMTIPS · Vellum tips](https://www.sidefx.com/docs/houdini/vellum/vellumtips.html)
- [C-VELLUM · Houdini Vellum](https://tokeru.com/cgwiki/HoudiniVellum.html)
