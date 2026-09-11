# 用非破坏 USD 变体组织资产

ID: `recipe-usd-variants` · Skill: `houdini-solaris` · **recipe-design-not-runtime-tested**

## 输入
目标stage、prim paths、资产layer、reference/payload、variant、单位/时间、材质/灯光/相机。

## 最小网络意图
`Asset layers → Variant composition → Shot overrides → Export`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
variant set/name、选择、layer强度、引用路径

## 执行
1. 确定变体职责和默认选择，避免把不同资产版本混入同一不稳定路径。
2. 在shot层进行覆盖，保留源资产。
3. 检查每个变体的依赖和材质，再输出场景。

## 验收
- 切换变体时prim结构和依赖符合契约。
- 原资产不被覆盖，默认选择可复现。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../21-solaris.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [S-LOPNODE · hou.LopNode](https://www.sidefx.com/docs/houdini/hom/hou/LopNode.html)
- [C-LOPS · Houdini LOPs](https://tokeru.com/cgwiki/HoudiniLops.html)
