---
name: houdini-cli
description: 通过 houdini-cli 获取 Houdini 领域技能、查询模块与任务配方 Wiki，按需查询或修改节点网络、执行场景脚本，以及初始化 MCP、启动应用桥接和诊断环境。
---

使用终端中的 `houdini-cli`。以用户的目标任务为生命周期单位：任务内复用应用、桥接和 MCP，避免每个工具调用重新启动它们。

遇到 Houdini 模块、节点工作流、模拟、渲染或故障任务时，先通过 CLI 学习，再连接现场执行：

1. `houdini-cli skills list` 查看领域说明，`houdini-cli skills read houdini-agent` 读取知识路由；按任务读取匹配技能，例如 `houdini-cli skills read houdini-vellum`。
2. `houdini-cli wiki search "穿透" --limit 3` 查询用户问题；多词无命中时改用模块名或关键术语。用返回的页面 id 执行 `houdini-cli wiki read 12-vellum` 或 `houdini-cli wiki read recipes/cloth-penetration`，只读取相关页面。`wiki list` 可查看完整目录。
3. 技能中的相对 Wiki 链接可用 `wiki read` 读取；其他依赖通过 `houdini-cli skills read houdini-agent templates/acceptance.json` 等相对资源路径获取。`skills read` 返回资源目录；Python 查询器的知识检索步骤可直接使用 `wiki search`，无需安装 Python。需要运行辅助脚本时，先安装技能资源并核对脚本说明与 Python 环境。
4. 需要把技能持久安装到项目时使用 `houdini-cli skills install --name houdini-vellum --target <project>`；自动包含 `houdini-agent` 的 Wiki、示例、工具及自身 CLI skill，保证相对引用完整。默认不带 `--name` 仍只安装 `houdini-cli`。

以上知识命令离线运行，无需 Houdini、许可证、setup 或 MCP 会话。知识说明是学习资料；执行前仍须读取现场工具 schema、节点类型和参数，并以真实 cook、缓存或渲染结果验收。

多步骤任务先 `session status` 查看已有会话，然后 `session start <task-name> --launch-app`。同名任务复用会话；应用已运行时优先复用。不同目标占用同一个 CLI 状态目录时返回冲突，应协调原任务，不能结束它来抢占连接。环境只在缺失或损坏时 setup，无需每个任务重新安装。

任务中的工具命令都带 `--session <task-name>`，例如 `houdini-cli --session shot-01 tools list` 和 `houdini-cli --session shot-01 tools call <name> --args-file args.json`。规划、检查、修改、渲染、验收和短暂停顿期间保持会话。简单的单次只读查询可以使用没有会话的一次性调用；已有任务会话时 CLI 会阻止另开一次性 MCP。

任务完成后选择释放时机：

- 仍有相关步骤、短期继续处理或正在渲染/cook 时保留任务会话。用 `session status` 检查忙闲状态；进行中的请求不会因空闲超时被关闭。
- 目标已验收且暂时不用 MCP 时执行 `session end <task-name>`，释放 MCP 并保留应用与桥接。
- 只有本任务启动的应用、任务已完成、没有未保存内容/后台工作且不再需要交给用户继续使用时，才考虑 `session end <task-name> --close-app`。它核验进程归属，只发送正常窗口关闭请求，保留原生保存提示；返回保留/待处理状态就如实报告，不强杀、不自动丢弃内容。

用户原先打开或其他任务使用的应用保持打开。无归属证据和后台模式应用不会被自动关闭。默认 MCP 空闲回收为 30 分钟，可在 start 时用 `--idle-timeout <seconds>` 调整；回收只影响 MCP，不关闭应用。会话失联/调用超时先核对应用状态，显式重新建立会话时不重放已提交操作。

尚未初始化时运行 `doctor`；缺环境时检查 `setup --help`，再执行 `setup`。有现成定制 MCP 时用 `setup --source <directory>` 复用它，CLI 将依赖和兼容补丁放在自己的状态目录。任务启动流程为新 Houdini 进程加载桥接；已有进程未启用桥接时先协调启用，保留场景，不为重新接入而重启应用。Houdini 程序和许可证通过 SideFX 安装器提供，诊断结果应区分安装问题、许可证问题和连接失败。

用 `tools list` 获取当前工具，再 `tools inspect <name>` 查看输入 schema。通过 `tools call <name> --args-file <json-file>` 传入 UTF-8 JSON 对象，或用 `--stdin`；`call` 是简写。多步操作可用 `batch <json-file>`，格式 `[{"tool":"名称","args":{}}]`，首次失败即停止。

先读取节点网络与场景状态，再修改用户指定的节点。构建或修改网络后检查连接、参数、cook 错误和实际输出；渲染/导出以生成的结果验收。保留当前 .hip 与已有节点，另存或覆盖按用户指示执行。

stdout 为 JSON；`ok:false` 或非零退出码表示失败，上游原始内容块保留在 `result`。超时/中断时操作结果可能未知，先查询 Houdini 状态再考虑重试。批次错误包含已完成项，避免重放它们。

`skills install --target <project>` 给其他项目安装此 skill；Claude 用 `--agent claude`。用户要求停用固定 MCP 时用 `integration disable-codex --dry-run` 查看将改变的条目，然后执行实际迁移。它保存备份，重启 Codex 生效。
