---
name: houdini-cli
description: 通过 houdini-cli 获取 Houdini 领域技能、查询模块与任务配方 Wiki，按需查询或修改节点网络、执行场景脚本，以及初始化 MCP、启动应用桥接和诊断环境。
---

# Houdini CLI

遇到 Houdini 模块、节点工作流、模拟、渲染或故障任务时，先通过 CLI 学习，再连接现场执行：

1. `houdini-cli skills list` 查看领域说明，`houdini-cli skills read houdini-agent` 读取知识路由；按任务读取匹配技能，例如 `houdini-cli skills read houdini-vellum`。
2. `houdini-cli wiki search "穿透" --limit 3` 查询用户问题；多词无命中时改用模块名或关键术语。用返回的页面 id 执行 `houdini-cli wiki read 12-vellum` 或 `houdini-cli wiki read recipes/cloth-penetration`，只读取相关页面。`wiki list` 可查看完整目录。
3. 技能中的相对 Wiki 链接可用 `wiki read` 读取；其他依赖通过 `houdini-cli skills read houdini-agent templates/acceptance.json` 等相对资源路径获取。`skills read` 返回资源目录；Python 查询器的知识检索步骤可直接使用 `wiki search`，无需安装 Python。需要运行辅助脚本时，先安装技能资源并核对脚本说明与 Python 环境。
4. 需要把技能持久安装到项目时使用 `houdini-cli skills install --name houdini-vellum --target <project>`；自动包含 `houdini-agent` 的 Wiki、示例、工具及自身 CLI skill，保证相对引用完整。默认不带 `--name` 仍只安装 `houdini-cli`。

以上知识命令离线运行，无需 Houdini、许可证、setup 或 MCP 会话。知识说明是学习资料；执行前仍须读取现场工具 schema、节点类型和参数，并以真实 cook、缓存或渲染结果验收。

多步骤任务先 `session status` 查看已有会话，然后 `session start <task-name> --launch-app`。同名任务复用会话；应用已运行时优先复用。不同目标占用同一个 CLI 状态目录时返回冲突，应协调原任务，不能结束它来抢占连接。环境只在缺失或损坏时 setup，无需每个任务重新安装。

## 调用现场工具

多步骤操作先 `session status`，再 `session start <task-name> --launch-app`；同名任务复用会话，应用已运行时优先复用。其他目标占用同一状态目录会冲突，协调原任务，不能结束它来抢连接。单次只读查询可用无会话调用；已有任务会话时 CLI 会阻止另开一次性 MCP。

任务内所有工具命令带 `--session <task-name>`。先 `tools list`，再 `tools inspect <实际名称>` 取输入 schema；同一环境已核对的 schema 可复用，环境变更后重新发现。候选工具名不保证存在。

用 `tools call <name> --args-file <file>` 传 UTF-8 JSON 对象，或用 `--stdin`；`call` 是简写。`batch <file>` 格式为 `[{"tool":"名称","args":{}}]`，按顺序执行、首错停止、没有回滚。同一桥接的调用保持串行。

先读取当前场景及目标节点，再按授权修改，保留当前 .hip 和无关节点；另存或覆盖按用户指示。节点内部名、参数、连接以现场为准。stdout 是 JSON；检查退出码、外层 `ok`、`result` 中 MCP `isError` 和内嵌业务错误，再读回连接、参数、cook 错误与真实输出。渲染/导出以实际产物验收。

在授权范围与预算内持续修复到请求结果及相关检查通过，无需为已授权可逆步骤逐次确认。超时/中断表示结果可能未知，先查应用、节点、文件与已完成项；不重放未知写操作或已成功的批次项。无法运行时保留可用产物与明确阻塞，不能用 JSON 成功文本代替运行证据。

## 会话释放

- 规划、修改、渲染、cook、验收和短暂停顿期间保留会话；用 `session status` 看忙闲。默认空闲回收 30 分钟，start 的 `--idle-timeout <seconds>` 可调整；运行中请求不因空闲超时关闭，回收只影响 MCP。
- 目标已验收且暂时不用 MCP 时，`session end <task-name>` 释放 MCP，默认保留应用和桥接。
- 仅本任务启动、无未保存内容/后台工作且无需交回用户继续使用的应用，才考虑 `session end <task-name> --close-app`。它核验归属并正常请求关闭，保留原生保存提示；待处理或保留状态如实报告，不强杀或丢弃内容。用户原先打开、其他任务使用、无归属证据及后台模式应用保持打开。

会话失联时先核对应用；显式重建会话不重放已提交操作。

## 缺失环境或连接故障

先 `doctor`；仅环境缺失/损坏时查 `setup --help` 再 `setup`，不为普通任务重装。有定制 MCP 时用 `setup --source <directory>`，依赖与兼容补丁在 CLI 状态目录。Houdini 和许可证由 SideFX 安装器提供；区分安装、许可证与连接失败。

启动流程只为新进程加载桥接；已有应用未启桥接时保留场景并协调启用，不为接入重启应用。桥接保持本地访问，不公开端口。

## 用户要求安装或迁移时

`skills install --target <project>` 安装此单文件技能；Claude 用 `--agent claude`。停用固定 MCP 时先用 `integration disable-codex --dry-run` 查看条目，再执行已授权迁移；它保存备份，重启 Codex 生效。这些操作不属于普通场景任务的前置步骤。
