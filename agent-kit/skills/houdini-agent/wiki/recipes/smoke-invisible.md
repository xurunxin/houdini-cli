# 烟雾不可见的分层排查

ID: `recipe-smoke-invisible` · Skill: `houdini-pyro` · **recipe-design-not-runtime-tested**

## 输入
源几何与持续时间、字段名/类型、体素尺寸、域/边界、碰撞、散热和外观需求。

## 最小网络意图
`Pyro Source → Rasterized fields → Pyro Solver → Cache → Material/render`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
字段名/类型、active bounds、源时段、显示/着色范围

## 执行
1. 逐层查密度/温度/速度字段是否存在、范围是否正确。
2. 数据缺失时修source/接线/cook；字段存在时才查display和shader。
3. 用简单灯光材质单帧渲染，不同时更改所有解算参数。

## 验收
- 定位首个缺字段或不可见环节。
- 缓存读回和实际渲染均能证明体积存在。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../13-pyro.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-PYRO · Pyro](https://www.sidefx.com/docs/houdini/pyro/index.html)
- [S-PYROSOLVER · Pyro Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/pyrosolver.html)
- [S-PYROLOOK · Pyro workflow/lookdev](https://www.sidefx.com/docs/houdini/pyro/lookdev.html)
- [C-PYRO · Smoke and Pyro (mixed/legacy)](https://tokeru.com/cgwiki/Smoke_and_Pyro.html)
