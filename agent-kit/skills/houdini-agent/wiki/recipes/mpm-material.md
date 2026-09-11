# 雪沙材料的小体积 MPM 测试

ID: `recipe-mpm-material` · Skill: `houdini-mpm` · **recipe-design-not-runtime-tested**

## 输入
材料目标（雪/沙/弹塑性等）、分辨率、尺度、碰撞、设备资源与当前安装能力。

## 最小网络意图
`Small material source + simple collider → MPM Solver → Cache`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
材料模型、采样、尺度、碰撞、设备要求

## 执行
1. 现场发现MPM节点和当前材料选项。
2. 同一小域测试下落、压缩与回弹，记录资源占用。
3. 通过后再扩展形状与数量；社区snow案例只作为目标参考。

## 验收
- 材料行为趋势符合目标。
- 版本/硬件要求与现场能力匹配，成本有测量。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../15-mpm.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-MPM · MPM](https://www.sidefx.com/docs/houdini/mpm/index.html)
- [S-VELLUM · Vellum](https://www.sidefx.com/docs/houdini/vellum/index.html)
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html)
- [E-MPM · Entagma: Smol MPM / Falling Snow](https://entagma.com/smol-mpm-falling-snow/)
