# CLI 超时后的不重放恢复流程

ID: `recipe-timeout-recovery` · Skill: `houdini-agent` · **recipe-design-not-runtime-tested**

## 输入
任务名、已存在会话、当前场景与未保存状态；当前工具列表及输入 schema；输出白名单目录。

## 最小网络意图
`Unknown result → Session/app status → Read target/output → Reconcile`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
任务名、原请求、已完成项、目标节点/文件、后台工作

## 执行
1. 保留原请求和超时日志，标记unknown。
2. 只读检查已有会话、应用状态和目标输出，防止第二个MCP抢占。
3. 状态确认后决定显式重连或继续未完成项；不能自动重新发送原写操作。

## 验收
- 重复创建/渲染被避免。
- 已完成、失败和未知项分开记录。

风险: `inspection-and-reconciliation`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../02-cli-contract.md) · [执行协议](../02-cli-contract.md)

## 来源
- [R-README · houdini-cli README](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/README.md)
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs)
- [R-SKILL · houdini-cli existing skill](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/skills/houdini-cli/SKILL.md)
- [R-SETUP · houdini-cli setup](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/houdini-setup.md)
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md)
- [R-INSTALL · houdini-cli skill installer](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/skills.mjs)
