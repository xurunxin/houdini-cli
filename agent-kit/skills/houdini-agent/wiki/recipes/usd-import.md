# SOP 资产进入 Solaris 的边界验证

ID: `recipe-usd-import` · Skill: `houdini-solaris` · **recipe-design-not-runtime-tested**

## 输入
目标stage、prim paths、资产layer、reference/payload、variant、单位/时间、材质/灯光/相机。

## 最小网络意图
`OUT_SOP → SOP Import → Stage inspection → USD output`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
prim路径、单位、purpose、transform、属性转primvar

## 执行
1. 指定稳定OUT和prim命名规则。
2. 在stage中核对prim类型、层级和transform，而不只看node参数。
3. 测试一份导出读回，确认相对依赖可解析。

## 验收
- SOP与USD尺寸/位置一致。
- prim路径和所需primvar在导出后保留。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../21-solaris.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/hom/usd_report.py)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [S-LOPNODE · hou.LopNode](https://www.sidefx.com/docs/houdini/hom/hou/LopNode.html)
- [C-LOPS · Houdini LOPs](https://tokeru.com/cgwiki/HoudiniLops.html)
