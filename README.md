# houdini-cli

以目标任务管理 houdini-cli 的应用和 MCP 生命周期。任务内复用同一应用和 MCP 进程，按目标完成、资源占用和用户后续使用决定保留或关闭。

## 推荐任务流程（v0.2）

```powershell
houdini-cli session start shot-01 --launch-app
houdini-cli --session shot-01 tools list
houdini-cli --session shot-01 tools inspect <工具名>
houdini-cli --session shot-01 tools call <工具名> --args-file args.json
houdini-cli session status shot-01
# 目标完成：释放 MCP，应用继续保留
houdini-cli session end shot-01
# 确认本任务启动的应用无未保存工作且不再需要时
# houdini-cli session end shot-01 --close-app
```

`--launch-app` 优先复用已有应用，只在没有对应应用时启动并记录进程归属。同名 start 幂等复用会话；一个 CLI 状态目录同时服务一个目标任务，其他目标会返回冲突。任务期间工具命令加 `--session`；已有会话时，省略该参数会失败，避免另开 MCP 抢占应用桥接。

`session end` 默认只关闭 MCP。`--close-app` 仅正常关闭本任务启动、PID/路径/创建时间仍匹配的 Windows GUI；原生保存提示不会被绕过。复用的应用、身份不明的进程、后台应用及不支持的平台均保留，并返回原因。Agent 应先检查未保存内容、后台渲染/cook 和后续用途，再决定关闭时机。应用桥接随应用保留。

会话仅在任务请求下创建，通过本机带随机凭据的通道供 CLI 调用，不注册为固定 Codex MCP。默认空闲 1800 秒回收 MCP，`session start --idle-timeout <seconds>` 可调整（1..86400）；进行中的请求不触发空闲回收。空闲回收、异常和中断均保留应用。超时后不自动重启/重试，先检查实际操作结果。

无任务会话时仍支持一次性 `tools/call/batch`；它们只在该次命令期间运行 MCP。下面的单次示例也可在命令前加入 `--session <task>`，在任务内复用连接。

## 安装和初始化

需要 Node.js 22+、uv、Git 和已安装、可启动的 Houdini。此仓库为私有，先认证有访问权限的 GitHub 账号：

```powershell
gh repo clone xurunxin/houdini-cli
cd houdini-cli
npm ci
npm install --global .
houdini-cli doctor
houdini-cli setup --dry-run
houdini-cli setup --timeout 180000
houdini-cli app launch
houdini-cli doctor --connect
houdini-cli tools list
```

也可用 `npm install --global git+ssh://git@github.com/xurunxin/houdini-cli.git`（需要 GitHub SSH 权限）。无需发布 npm registry 包。

Windows 新环境可执行 `pwsh -NoProfile -File scripts/install.ps1 -InstallPrerequisites`，通过 winget 补齐 Node.js、uv，再安装 CLI 和执行 setup。Git 缺失时先安装 Git。Houdini 及许可证由 [SideFX 安装器](https://www.sidefx.com/download/)提供。`-SkipSetup` 仅安装 CLI；`-Project <path>` 同时安装项目 skill。

新环境 setup 获取固定上游版本、在 CLI 状态目录准备依赖和兼容处理，并生成本次会话的应用启动插件。复用已有定制源码：

```powershell
houdini-cli setup --source "D:\Tools\houdini-mcp" --app-path "C:\Program Files\Side Effects Software\Houdini 22.0.368\bin\houdini.exe"
```

原源码目录不作为依赖安装或补丁写入目标；环境与补丁副本放在 CLI 自己的目录。详细来源、兼容范围和安装逻辑见 [Houdini 初始化](docs/houdini-setup.md)。默认端口 9877，仅支持本机 loopback；`setup --port <n>` 保存端口。

## 工具操作

```powershell
houdini-cli tools list
houdini-cli tools inspect <工具名>
houdini-cli tools call <工具名> --args-file args.json
```

`tools list --full` 输出所有说明与 schema；`call <工具名>` 是简写。参数为 JSON 对象，可选 `--args '<JSON>'`、`--args-file` 或 `--stdin`；PowerShell 推荐 UTF-8 JSON 文件。不同现成源码可能暴露不同工具，以实时发现为准。

`batch calls.json` 接受 `[{"tool":"名称","args":{}}]`，顺序运行并共享一个短暂 MCP 会话。首个错误停止并报告已完成项；应用改动不自动回滚。`resources list/read` 访问上游支持的资源。

JSON stdout 返回业务结果，`--verbose` 向 stderr 输出上游诊断。退出码 `0` 成功，`1` 环境/运行/工具错误，`2` 参数错误。MCP `isError` 转成 `TOOL_ERROR` 并保留内容。一次性会话默认超时 60 秒，任务模式每个请求默认超时 60 秒，用 `--timeout 180000` 调整；超时/中断后先查询节点和场景状态，再决定是否重试，避免重复渲染或修改。

## 项目 skills 与迁移

```powershell
houdini-cli skills install --target "D:\MyProject"
houdini-cli skills install --target "D:\MyProject" --agent all --dry-run
houdini-cli integration disable-codex --dry-run
# 确认 CLI 实际调用成功后迁移
houdini-cli integration disable-codex
```

skills 默认安装到调用者项目 `.agents/skills/houdini-cli/SKILL.md`；`--agent claude` 使用 `.claude/skills`，`all` 安装两处。省略 `--target` 使用当前目录。冲突的定制 skill 需要 `--force` 才更新；保留无关文件并拒绝 symlink/junction 逃逸。

迁移命令仅将 Codex 的 `houdini-mcp` / `houdini` 固定表设为 `enabled = false`，在原配置旁保存唯一备份，保留其他服务。重启 Codex 后生效；恢复时将相应字段改为 `true`。setup 本身不修改 Codex 配置。

状态默认位于用户本地数据目录 `houdini-cli`；支持 `--home <directory>` 或 `HOUDINI_CLI_HOME`。`config` 查看实际配置。

## Houdini Agent Wiki 与领域 Skills

[Houdini Agent Kit](agent-kit/README.md) 的 Wiki、领域 Skills、HOM/VEX 示例和辅助工具随 CLI 分发。CLI 自身 skill 会引导 agent 先检索知识，再发现现场能力并执行。

从任意目录查询，无需 Houdini、MCP、setup 或 Python：

```powershell
houdini-cli skills list
houdini-cli skills read houdini-agent
houdini-cli skills read houdini-vellum
houdini-cli wiki search "穿透" --limit 3
houdini-cli wiki read recipes/cloth-penetration
houdini-cli wiki list
houdini-cli skills read houdini-agent examples/hom/runtime_probe.py
houdini-cli skills install --name houdini-vellum --target "D:/MyProject" --dry-run
houdini-cli skills install --name houdini-vellum --target "D:/MyProject"
```

`skills read <name> [resource]` 返回技能正文或相对资源内容；`wiki search` 按字面关键词搜索正文，返回有限命中摘要，再按 id 读取页面。命令输出 JSON。`skills install --name <技能名>` 自动安装 CLI skill 与 `houdini-agent` 依赖及完整资源，支持原有 `--agent`、`--force` 和冲突保护；默认不带 `--name` 仍只安装 CLI skill。辅助 Python 脚本仅在需要实际运行时要求 Python 3.10+。

[Wiki 目录](agent-kit/skills/houdini-agent/wiki/README.md) · [集成说明](agent-kit/INTEGRATION.md) · [验收边界](agent-kit/VALIDATION.md)。知识库和离线测试不代表已通过 Houdini 场景编辑、模拟或渲染验收。

## 开发和验收

```powershell
npm ci
npm test
npm run check
npm pack --dry-run
```

测试覆盖 MCP stdio 生命周期、分页、工具错误、超时、技能冲突/路径隔离和精确配置迁移，并有 Houdini 初始化与补丁测试。实际应用结果见 [验收记录](docs/validation.md)。主要验收平台是 Windows；其他平台及许可证类型须做独立目标环境验证。

上游为 [capoomgit/houdini-mcp](https://github.com/capoomgit/houdini-mcp)，客户端使用 [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk/tree/v1.x)。来源和许可证见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
