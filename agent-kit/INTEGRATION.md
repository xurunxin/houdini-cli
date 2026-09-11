# 与 xurunxin/houdini-cli 接入

## 采用加法集成，不改动已有 CLI

本包以 `agent-kit/` 子目录增量接入 `xurunxin/houdini-cli`，通过独立分支和 PR 审查；不直接更新主分支，不修改 CLI 实现和已有安装行为。也可以单独复制本目录维护。

仓库结构：

```text
houdini-cli/
  src/                            # 原有CLI，保持不变
  skills/houdini-cli/SKILL.md      # 原有环境/任务生命周期skill，保持不变
  agent-kit/
    README.md
    tools/install_kit.py
    skills/houdini-agent/          # 自包含hub，内含wiki/index/tools/examples
    skills/houdini-*/SKILL.md      # 可选的领域技能
    tests/
```

原有 `houdini-cli skills install` 目前仅复制单个 `SKILL.md`。不能假装调用它就会安装本包的子目录。请使用本包独立安装器；它会递归复制每个选定skill的文件，并保留相关相对路径。

```powershell
# 在本包根目录
python tools/install_kit.py --target "D:/target-project" --profile core --agent codex
```

`core`推荐个人常用环境：只加入一个路由描述，全部知识仍随hub安装。`all`适合希望按领域触发的Agent；它不意味着每次任务要加载20个skill全文。

## Codex / Claude 共存

默认Codex目录 `.agents/skills`；`--agent claude`为`.claude/skills`，`--agent all`两处。安装后按客户端的skill发现机制刷新或重新打开项目。此包不配置固定MCP，继续使用CLI按目标任务建立会话。

## 从主仓库使用

仓库根 README 提供 `agent-kit/README.md` 入口。以下命令从仓库根目录运行：

```powershell
python agent-kit/tools/install_kit.py --target "D:/MyProject" --agent codex --profile core --dry-run
python agent-kit/tools/install_kit.py --target "D:/MyProject" --agent codex --profile core
python agent-kit/skills/houdini-agent/tools/query.py search "布料穿透" --limit 3
```

现有 `package.json` 的发布文件集合不包含 `agent-kit/`，本次不改动它；知识包从仓库检出目录安装，而不是假定全局 npm 安装已经包含本包。未来要把本包接入 CLI 自身安装器或 npm 包，应在单独 PR 中扩展递归复制、冲突预检、打包文件集、symlink/junction 保护和测试，而不是仅修改 Skill 里的相对路径。

## 更新与回退

安装前dry-run；遇到定制冲突审查差异再`--force`。备份仅在有文件被替换时写入目标项目的`.houdini-agent-kit-backups/<run>`。工具不自动删除旧版或无关文件，避免丢失用户新增内容。

回退时从对应备份逐文件审查恢复。新装文件是否删除取决于它是否由本次任务引入；不要整目录删除用户有可能继续编辑过的skill。整包安装不具备跨文件事务性。

## 尚未完成的现场工作

PR 只接入可检索、可安装、可测试的知识包与文档入口；未修改 CLI 本身，未执行 Houdini 编辑或渲染。现场验收按 [现场测试矩阵](skills/houdini-agent/wiki/target-smoke.md) 逐项进行。

基线：[现有安装器](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/skills.mjs)。
