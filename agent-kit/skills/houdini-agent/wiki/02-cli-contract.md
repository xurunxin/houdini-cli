# houdini-cli 会话、工具与安全契约

ID: `cli-contract` · 领域: CLI / HOM · Skill: `houdini-agent`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
在现有 CLI 上执行，不发明 houdini-cli 自带的建模/渲染子命令。

## 输入契约
任务名、已存在会话、当前场景与未保存状态；当前工具列表及输入 schema；输出白名单目录。

## 推荐操作
1. 先 session status；目标任务可用时 session start <task> --launch-app。任务中所有 tools/call/batch 都带 --session。不要结束其他目标的会话抢连接。
2. 先 tools list，再 tools inspect <实际工具名>。工具名和参数只以实时 schema 为准。get_scene_info 等仅是已知候选，不保证定制服务均提供。
3. 先读场景，专用工具优先；仅缺能力时使用经检查的 execute_houdini_code。PowerShell 用 UTF-8 JSON 文件或 --stdin，避免多层引号。
4. 逐次串行执行。batch 只有顺序、首错停止，没有事务回滚。工具超时后记录 outcome=unknown，检查目标节点/文件/任务状态，不重放创建、模拟和渲染。
5. 任务验收后 session end <task> 只释放 MCP。默认保留应用、桥接、用户场景；不自动 --close-app、不强杀、不公开桥接端口。

## 验收条件
- 退出码、外层 ok、MCP isError、内嵌业务错误都检查。
- 实时读回网络与产物，而不只依据 stdout 的成功文本。
- 记录已完成项、未知项、下一次安全检查。

## 症状 → 优先检查
**一调用就掉线**：排查第二个 MCP 客户端；单桥接最新连接会替换旧连接，多个 home 不等于隔离应用。
**已有应用无法连接**：CLI 不会向已有未启桥接的进程注入；保留现场并协调启用。
**工具超时**：请求结果未知，不代表 Houdini 已停止；延长 CLI 超时也不保证上游无独立超时。

## 版本与边界
绑定 CLI 0.2.0 / commit 57a8e81；CLI 默认桥接为 loopback:9877，不照抄上游的 9876。现有 skills install 只复制原有单个 SKILL.md，本包用独立安装器。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`get_scene_info`、`execute_houdini_code`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [R-README · houdini-cli README](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/README.md) — file；
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs) — file；
- [R-SKILL · houdini-cli existing skill](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/skills/houdini-cli/SKILL.md) — file；
- [R-SETUP · houdini-cli setup](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/houdini-setup.md) — file；
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md) — file；
- [R-INSTALL · houdini-cli skill installer](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/skills.mjs) — file；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
