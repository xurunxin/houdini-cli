# 节点参数设置部分失败后的恢复

ID: `recipe-parameter-failure` · Skill: `houdini-agent` · **recipe-design-not-runtime-tested**

## 输入
任务名、已存在会话、当前场景与未保存状态；当前工具列表及输入 schema；输出白名单目录。

## 最小网络意图
`get_parameter_schema → set_parameters → read back`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
内部参数名、类型与tuple、菜单token、failed清单

## 执行
1. 先读取当前参数schema与已设值。
2. 只提交存在、类型匹配的参数；记录返回result.failed，不因status=success忽略。
3. 已成功项不重放，修正失败项后再次读回，并进行领域验收。

## 验收
- failed清单为空或逐项说明未执行原因。
- 成功参数读回一致，所需效果检查通过。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../02-cli-contract.md) · [执行协议](../02-cli-contract.md)

## 来源
- [R-README · houdini-cli README](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/README.md)
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs)
- [R-SKILL · houdini-cli existing skill](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/skills/houdini-cli/SKILL.md)
- [R-SETUP · houdini-cli setup](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/houdini-setup.md)
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md)
- [R-INSTALL · houdini-cli skill installer](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/skills.mjs)
- [R-TOOLS · Pinned upstream tool implementations](https://github.com/capoomgit/houdini-mcp/blob/de4fd93acc207fc57c02b330d421461f5963a945/houdini_mcp_server.py)
