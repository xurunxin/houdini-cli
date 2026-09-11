# 在独立任务空间验证创建、连线与 cook

ID: `recipe-sop-smoke` · Skill: `houdini-agent` · **recipe-design-not-runtime-tested**

## 输入
目标 node path 或父网络 path，效果关键词，节点类型候选；不要把界面标签当作内部名称。

## 最小网络意图
`Box → Transform → Null OUT`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
box尺寸tuple、transform平移tuple、节点类型全名

## 执行
1. 先read-only probe与工具schema确认连接，取得用户对小样例修改与cook许可。
2. 将build-sop-smoke配置的allow_write和allow_cook设true，保持任务名唯一。
3. 封装脚本后调用一次；若超时或同名空间存在，改为查询，不重复创建。

## 验收
- OUT包围盒与尺寸/平移计算结果一致。
- 无清空场景、删除、保存或渲染；输出节点留给用户检查。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../03-runtime-discovery.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/hom/build_sop_smoke.py)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [S-NODE · hou.Node](https://www.sidefx.com/docs/houdini/hom/hou/Node.html)
- [S-OPNODE · hou.OpNode](https://www.sidefx.com/docs/houdini/hom/hou/OpNode.html)
- [S-NODETYPE · hou.NodeType](https://www.sidefx.com/docs/houdini/hom/hou/NodeType.html)
- [S-PARM · hou.Parm](https://www.sidefx.com/docs/houdini/hom/hou/Parm.html)
- [C-PYTHON · Houdini Python](https://tokeru.com/cgwiki/HoudiniPython.html)
- [S-BOX · Box SOP](https://www.sidefx.com/docs/houdini/nodes/sop/box.html)
- [S-XFORM · Transform SOP](https://www.sidefx.com/docs/houdini/nodes/sop/xform.html)
