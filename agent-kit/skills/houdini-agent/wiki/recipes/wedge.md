# 参数 Wedge 的安全批量产出

ID: `recipe-wedge` · Skill: `houdini-pdg` · **recipe-design-not-runtime-tested**

## 输入
输入清单、work item属性、依赖、输出文件命名、scheduler、许可证/内存/设备并发预算。

## 最小网络意图
`Wedge → Single proven work item → Declared outputs → Gather`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
item属性、文件名、依赖、scheduler、并发资源

## 执行
1. 先手动验证一个变体。
2. 输出名加入资产/版本/item/seed，声明依赖并设置并发上限。
3. 只对状态已知且可重复任务做重试，保留每项日志。

## 验收
- 不同item不会覆盖同一文件。
- 失败项可隔离重跑，成功项来源可追溯。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../26-pdg.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-TOPS · PDG / TOPs](https://www.sidefx.com/docs/houdini/tops/index.html)
- [S-TOPROP · ROP Geometry TOP](https://www.sidefx.com/docs/houdini/nodes/top/ropgeometry.html)
- [C-TOPS · Houdini TOPs](https://tokeru.com/cgwiki/HoudiniTops.html)
