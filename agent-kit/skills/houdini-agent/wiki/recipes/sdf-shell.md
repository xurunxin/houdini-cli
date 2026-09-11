# 用 SDF 合成壳体或融合形状

ID: `recipe-sdf-shell` · Skill: `houdini-volumes` · **recipe-design-not-runtime-tested**

## 输入
字段名、标量/向量、fog或level set、体素尺寸、transform、active bounds、是否封闭几何。

## 最小网络意图
`Clean closed meshes → VDB from Polygons → VDB align/combine → Convert VDB`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
level set类型、体素尺寸、窄带、transform、iso阈值

## 执行
1. 先验证输入封闭性和最薄特征是否可由体素表达。
2. SDF在统一空间与网格条件下组合，必要时重采样。
3. 转换回网格后检查边缘、体积损失和面数，再决定重拓扑。

## 验收
- 字段语义未被混成fog，包围盒与目标吻合。
- 薄部件未无意消失，网格可用于下游。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../08-volumes.md) · [执行协议](../02-cli-contract.md)

## 来源
- [C-VOLUME · Houdini Volumes](https://tokeru.com/cgwiki/HoudiniVolumes.html)
- [S-PYROLOOK · Pyro workflow/lookdev](https://www.sidefx.com/docs/houdini/pyro/lookdev.html)
- [S-GEO · hou.Geometry](https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html)
