# HOM 反射、节点版本与参数发现

ID: `runtime-discovery` · 领域: HOM · Skill: `houdini-agent`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
在动作前确定实际节点类型、版本、连接口和可用参数。

## 输入契约
目标 node path 或父网络 path，效果关键词，节点类型候选；不要把界面标签当作内部名称。

## 推荐操作
1. 运行 runtime_probe.py 获取当前版本、Python、UI、许可证类别与帧率；运行 discover_node_types.py 用关键词和 category 搜索已安装类型。
2. 检查类型的 nameComponents、description、输入输出数量；多版本或命名空间冲突时先选择兼容目标。不要按字符串排序猜“最新”。
3. 对真实节点用 inspect_node.py 读取 parm 模板、连接和输入输出名称。动态菜单和参数求值可能触发脚本/依赖，默认不自动执行。
4. 创建基础 SOP 时可明确 exact_type_name；对高层 HDA 不随意关闭初始化脚本。缺少节点时记录版本/Labs/插件依赖，禁止用同名但语义不同节点替代。
5. 设置后读回参数和连接；参数表达式、菜单 token、tuple 和 multiparm 分别处理。

## 验收条件
- 记录 category/type 全名、选用版本、节点 path。
- 每个写入参数都有现场存在性与类型证据。
- 旧教程的参数没有被静默省略。

## 症状 → 优先检查
**显示标签对但 parm 为 None**：查实际内部 name，不猜 snake_case。
**createNode 自动变成别的版本**：检查 namespace precedence 和 exact_type_name；显式选择后再确认 type。
**HOM 方法缺失**：查当前版本及 Node/OpNode/SopNode/LopNode 区分，不照搬别的上下文对象。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`NodeType`、`ParmTemplate`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-NODE · hou.Node](https://www.sidefx.com/docs/houdini/hom/hou/Node.html) — selected-sections；
- [S-OPNODE · hou.OpNode](https://www.sidefx.com/docs/houdini/hom/hou/OpNode.html) — selected-sections；
- [S-NODETYPE · hou.NodeType](https://www.sidefx.com/docs/houdini/hom/hou/NodeType.html) — selected-sections；
- [S-PARM · hou.Parm](https://www.sidefx.com/docs/houdini/hom/hou/Parm.html) — selected-sections；
- [C-PYTHON · Houdini Python](https://tokeru.com/cgwiki/HoudiniPython.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
