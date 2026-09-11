# USD 材质绑定不生效的排查

ID: `recipe-usd-binding` · Skill: `houdini-solaris` · **recipe-design-not-runtime-tested**

## 输入
目标stage、prim paths、资产layer、reference/payload、variant、单位/时间、材质/灯光/相机。

## 最小网络意图
`Composed stage → Material path → Binding resolution → Render`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
prim匹配、材质path、层强度、collection/inheritance、delegate

## 执行
1. 在最终stage确认目标prim与材质存在。
2. 区分直接、继承、collection和更强layer绑定；usd_report只列直接关系，不假装解析全部。
3. 检查渲染器是否支持材质，再低分辨测试。

## 验收
- 最终绑定有解析证据，而不只是存在一根线。
- 测试图中目标对象使用预期材质。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../21-solaris.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [S-LOPNODE · hou.LopNode](https://www.sidefx.com/docs/houdini/hom/hou/LopNode.html)
- [C-LOPS · Houdini LOPs](https://tokeru.com/cgwiki/HoudiniLops.html)
