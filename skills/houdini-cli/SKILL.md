---
name: houdini-cli
description: 通过 houdini-cli 按需查询或修改 Houdini 节点网络、执行场景脚本，以及初始化 Houdini MCP、启动应用桥接和诊断环境。
---

使用终端中的 `houdini-cli`。每条命令打开短暂 MCP 会话，结束后关闭；Houdini 应用与本机桥接单独运行。

先运行 `doctor`；缺环境时检查 `setup --help`，再执行 `setup`。有现成定制 MCP 时用 `setup --source <directory>` 复用它，CLI 将依赖和兼容补丁放在自己的状态目录。`app launch` 为本次 Houdini 会话加载桥接。Houdini 程序和许可证通过 SideFX 安装器提供，诊断结果应区分安装问题、许可证问题和连接失败。

用 `tools list` 获取当前工具，再 `tools inspect <name>` 查看输入 schema。通过 `tools call <name> --args-file <json-file>` 传入 UTF-8 JSON 对象，或用 `--stdin`；`call` 是简写。多步操作可用 `batch <json-file>`，格式 `[{"tool":"名称","args":{}}]`，首次失败即停止。

先读取节点网络与场景状态，再修改用户指定的节点。构建或修改网络后检查连接、参数、cook 错误和实际输出；渲染/导出以生成的结果验收。保留当前 .hip 与已有节点，另存或覆盖按用户指示执行。

stdout 为 JSON；`ok:false` 或非零退出码表示失败，上游原始内容块保留在 `result`。超时/中断时操作结果可能未知，先查询 Houdini 状态再考虑重试。批次错误包含已完成项，避免重放它们。

`skills install --target <project>` 给其他项目安装此 skill；Claude 用 `--agent claude`。用户要求停用固定 MCP 时用 `integration disable-codex --dry-run` 查看将改变的条目，然后执行实际迁移。它保存备份，重启 Codex 生效。
