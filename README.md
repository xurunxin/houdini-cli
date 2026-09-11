# houdini-cli

将 Houdini MCP 转为按需 CLI。Agent 从终端发现实时工具 schema 并执行操作，命令完成、失败或超时后关闭自己的 MCP 子进程；Houdini 与应用内本机桥接单独运行。

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

JSON stdout 返回业务结果，`--verbose` 向 stderr 输出上游诊断。退出码 `0` 成功，`1` 环境/运行/工具错误，`2` 参数错误。MCP `isError` 转成 `TOOL_ERROR` 并保留内容。默认会话超时 60 秒，用 `--timeout 180000` 调整；超时/中断后先查询节点和场景状态，再决定是否重试，避免重复渲染或修改。

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

## 开发和验收

```powershell
npm ci
npm test
npm run check
npm pack --dry-run
```

测试覆盖 MCP stdio 生命周期、分页、工具错误、超时、技能冲突/路径隔离和精确配置迁移，并有 Houdini 初始化与补丁测试。实际应用结果见 [验收记录](docs/validation.md)。主要验收平台是 Windows；其他平台及许可证类型须做独立目标环境验证。

上游为 [capoomgit/houdini-mcp](https://github.com/capoomgit/houdini-mcp)，客户端使用 [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk/tree/v1.x)。来源和许可证见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
