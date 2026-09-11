# 将代理刚体模拟回传到高模

ID: `recipe-rbd-transfer` · Skill: `houdini-rbd` · **recipe-design-not-runtime-tested**

## 输入
带稳定name的碎片、packed几何、碰撞代理、约束几何与属性、驱动/静态物体。

## 最小网络意图
`High-res pieces + Sim proxy transforms → Transform transfer → OUT_RENDER`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
piece name、packed transform、pivot、rest匹配

## 执行
1. 统计高模与代理name集合并比较缺失/重复。
2. 验证一个碎片的rest位置与变换，不重复应用对象层transform。
3. 扩展全体后检查始帧、冲击帧和结束帧。

## 验收
- piece映射完整且唯一。
- 高模和代理刚性运动一致，无双重变换。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../11-rbd.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-RBD · Destruction](https://www.sidefx.com/docs/houdini/destruction/index.html)
- [S-BULLET · RBD Bullet Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/rbdbulletsolver.html)
