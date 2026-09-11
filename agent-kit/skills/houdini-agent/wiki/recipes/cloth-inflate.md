# 约束驱动的充气或软壳原型

ID: `recipe-cloth-inflate` · Skill: `houdini-vellum` · **recipe-design-not-runtime-tested**

## 输入
模拟几何、约束流、碰撞流；边长分布、厚度、质量、pin与目标动画、预期材料。

## 最小网络意图
`Closed input → Appropriate Vellum constraints → Animated target → Solver`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
封闭性、压力/体积约束、碰撞、质量、拓扑

## 执行
1. 在当前版本Help中确认所选约束支持的表示及目标参数。
2. 先静态小压力/目标测试，检查体积保持与固定区域。
3. 确认行为后动画化目标并检查整个变化区间。

## 验收
- 无意外泄漏/爆炸，约束和输入匹配。
- 目标动画对输出的影响可解释。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../12-vellum.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-VELLUM · Vellum](https://www.sidefx.com/docs/houdini/vellum/index.html)
- [S-VELLUMSOLVER · Vellum Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/vellumsolver.html)
- [S-VELLUMTIPS · Vellum tips](https://www.sidefx.com/docs/houdini/vellum/vellumtips.html)
- [C-VELLUM · Houdini Vellum](https://tokeru.com/cgwiki/HoudiniVellum.html)
