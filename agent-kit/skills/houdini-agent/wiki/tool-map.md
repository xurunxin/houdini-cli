# 已核对的工具候选与调用边界

**这不是你现场的工具列表或可直接发送的schema。** 它来自固定上游源码的部分函数；实际仍必须 `tools list → tools inspect`。自定义源可能增删或改变工具。

| 候选工具 | 风险 | 源码签名摘要（? 为可选） | 必查事项 |
| --- | --- | --- | --- |
| `get_scene_info` | scene-inspection | `按实时schema` | 读取场景概要；当前代码仓库的只读smoke候选。 |
| `get_parameter_schema` | inspection-with-evaluation | `path; pattern?; offset?; limit?` | 读取真实节点参数；可能执行参数求值/菜单相关逻辑，限定范围。 |
| `get_geometry_info` | may-cook | `path` | 点/面/属性/包围盒概要；可能cook。 |
| `get_geometry_data` | may-cook | `path; element?; attributes?; start?; limit?` | 分页值读取；固定上游limit有上限，仍以现场schema为准。 |
| `find_error_nodes` | last-cook-inspection | `root_path?; include_warnings?` | 读取上次cook错误，不强制cook；没有错误不证明数据新鲜。 |
| `connect_nodes` | scene-write | `from_path; to_path; input_index?; output_index?` | 两个节点同网络；0-based端口，检查实际输入语义。 |
| `disconnect_node_input` | scene-write | `path; input_index?` | 断开输入，可能改变下游结果。 |
| `set_parameters` | scene-write | `path; parameters(object)` | 检查result.failed；状态success仍可能部分失败。 |
| `set_node_flags` | scene-write | `path; display?; render?; bypass?; template?` | 仅设置明确传入项，检查unsupported。 |
| `layout_network` | scene-write-ui | `path` | 移动指定网络所有子节点，不能擅自重排无关用户网络。 |
| `cook_node` | may-expensive-cook | `path` | force cook，可能很贵或推进上游状态。 |
| `create_wrangle` | scene-write-and-cook | `parent_path; vex_code; name?; run_over?; input_node?` | 创建并立即验证Wrangle，检查validation，不只看创建成功。 |
| `set_wrangle_code` | scene-write-and-cook | `path; vex_code; validate?` | 替换现有代码；默认重新cook，先保存旧代码/意图。 |
| `delete_node` | destructive | `path` | 本包不自动调用；需要明确目标、权限及可恢复计划。 |
| `execute_houdini_code` | arbitrary-python | `code` | 后备能力。固定上游把stdout包在文本里；需解析业务结果标记。 |
| `render_single_view` | scene-and-file-side-effects | `orthographic?; rotation?; render_path?; render_engine?; karma_engine?` | 固定上游提供此工具，但不能把自动取景当成批准相机的正式渲染；执行前审查实现与输出。 |

## 两层不同的参数发现
`tools inspect set_parameters`查询MCP工具的JSON结构；`get_parameter_schema`查询Houdini节点自身的参数。两者不能互相代替。

## 成功的四个层次
CLI进程退出成功 → MCP请求成功 → 上游业务操作成功 → 数据/产物/艺术目标通过。每一层都需要证据。

## Python结果
原创脚本打印 `HOUDINI_AGENT_RESULT=<JSON>`；本包检查器识别它，包括固定上游的stdout文本包装。其他自由文本结果保持unknown，不臆测成功。参数部分失败、VEX validation错误、unsupported字段另行核对。

来源：[R-TOOLS 固定源码](https://github.com/capoomgit/houdini-mcp/blob/de4fd93acc207fc57c02b330d421461f5963a945/houdini_mcp_server.py)、[CLI接口](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs)。
