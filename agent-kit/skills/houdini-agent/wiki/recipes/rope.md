# 绳索/枝条的柔性运动

ID: `recipe-rope` · Skill: `houdini-vellum` · **recipe-design-not-runtime-tested**

## 输入
模拟几何、约束流、碰撞流；边长分布、厚度、质量、pin与目标动画、预期材料。

## 最小网络意图
`Curve → Resample → Vellum hair/stretch-bend constraints → Solver`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
边长、质量、厚度、stretch/bend、pin目标

## 执行
1. 保持可控曲线采样，不把曲线作为cloth面处理。
2. 检查pin和目标变形，再测试低速和高速动作。
3. 模拟曲线后再Sweep渲染外形，避免高面数参与基础解算。

## 验收
- 约束对应曲线拓扑，固定端位置正确。
- 弯曲、伸长和碰撞在连续帧中可接受。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../12-vellum.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-VELLUM · Vellum](https://www.sidefx.com/docs/houdini/vellum/index.html)
- [S-VELLUMSOLVER · Vellum Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/vellumsolver.html)
- [S-VELLUMTIPS · Vellum tips](https://www.sidefx.com/docs/houdini/vellum/vellumtips.html)
- [C-VELLUM · Houdini Vellum](https://tokeru.com/cgwiki/HoudiniVellum.html)
