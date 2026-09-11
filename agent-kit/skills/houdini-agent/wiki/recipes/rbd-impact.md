# 刚体碰撞与约束破裂的最小测试

ID: `recipe-rbd-impact` · Skill: `houdini-rbd` · **recipe-design-not-runtime-tested**

## 输入
带稳定name的碎片、packed几何、碰撞代理、约束几何与属性、驱动/静态物体。

## 最小网络意图
`Fracture/name → Pack/configure → Constraints + proxy → RBD Bullet Solver → Cache`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
piece name、代理类型、active/animated、约束类型、阈值、子步

## 执行
1. 先无外力运行静止测试，消除初始重叠和约束长度错误。
2. 只加一个撞击体，检查代理碰撞和大块运动。
3. 最后调整约束破裂条件；用同一输入时段对比阈值。

## 验收
- 静止状态无初始爆炸。
- 破裂时序与冲击一致，渲染碎片可通过name映射回传。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../11-rbd.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-RBD · Destruction](https://www.sidefx.com/docs/houdini/destruction/index.html)
- [S-BULLET · RBD Bullet Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/rbdbulletsolver.html)
