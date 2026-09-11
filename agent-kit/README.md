# Houdini Agent Kit

**v0.1.0 · 中文 · 2026-09-11 · 对接 houdini-cli 0.2.0**

为 Agent 提供“任务检索 → 现场能力发现 → 最小操作 → 输出验收”的 Houdini 知识层。不是 Houdini 软件、许可证、全站文档镜像，也不是声称所有效果已通过验证的自动生成器。

## 从这里开始

人类阅读：[Wiki 首页](skills/houdini-agent/wiki/README.md) · [离线阅读器](wiki.html) · [快速上手](skills/houdini-agent/wiki/quickstart.md)。
Agent 入口：[houdini-agent/SKILL.md](skills/houdini-agent/SKILL.md)。
维护与集成：[接入已有仓库](INTEGRATION.md) · [维护流程](CONTRIBUTING.md) · [验收与边界](VALIDATION.md)。

## 包含什么

| 层 | 内容 | 用途 |
| --- | --- | --- |
| 知识卡 | 32 个领域页 | 输入、步骤、节点候选、常见故障、验收与来源 |
| 配方 | 40 个任务页 | 从具体问题定位最小网络意图、待查参数和检查方法 |
| Skills | 20 个 | 1 个总路由 + 19 个领域执行入口，可只安装总路由 |
| 示例 | 6 个 HOM 脚本 + 6 个 VEX 片段 | 现场探测、参数反射、受控小网络和常用属性计算 |
| 查询与验收工具 | 纯 Python 离线工具 | 中英检索、schema封装、结果检查、序列/证据清单检查 |
| 来源注册表 | 81 条 | 官方、CGWiki、John Kunz、Entagma及固定提交代码；逐条记录阅读深度 |

**知识不是运行证据。** 本环境无 Houdini/hython。HOM 示例只完成离线语法及可测试保护逻辑检查，VEX 未在 Houdini 编译，FX/渲染没有现场验收。源代码仓库自身已有只读查询验收，但不能据此宣称这些新配方已运行。详见 [VALIDATION](VALIDATION.md)。

v0.1 已通过 **64 项离线测试**与 **11 项阅读器检查**；本次仓库接入重新运行离线测试、生成同步检查和实包安装查询。阅读器的 11 项记录来自 v0.1 构建，未作为本次新跑结果。详情见验收记录。

## 安装到项目

需要 Python 3.10+。此包本身无需 Houdini 就能检索；真正执行场景仍需用户已安装和授权的 Houdini、现有 `houdini-cli` 及其依赖。

在仓库的 **`agent-kit/` 目录**（或独立解压后的本目录）运行，目标项目目录必须已存在：

```powershell
# 推荐：只激活一个路由 Skill，但保留全部 Wiki、配方和工具。
python tools/install_kit.py --target "D:/MyProject" --agent codex --profile core --dry-run
python tools/install_kit.py --target "D:/MyProject" --agent codex --profile core

# 需要分领域自动触发时安装全部 Skills；all 同时安装到 Codex 和 Claude 的目录。
python tools/install_kit.py --target "D:/MyProject" --agent all --profile all --dry-run
python tools/install_kit.py --target "D:/MyProject" --agent all --profile all
```

默认写入 `.agents/skills/houdini-agent/`；Claude 为 `.claude/skills/`。**不覆盖现有 `houdini-cli` Skill，不修改 CLI、Codex 全局配置、Houdini 环境文件或固定 MCP。**
同名内容冲突默认停止，先审查再考虑 `--force`；强制更新备份旧的冲突文件，保留无关文件，拒绝目标路径中的 symlink/junction/reparse point。安装按文件原子替换，不宣称跨整包事务；发生中断会报告已写文件。

## 离线快速查询

```powershell
python skills/houdini-agent/tools/query.py search "布料穿透" --limit 3
python skills/houdini-agent/tools/query.py search "USD材质不生效" --limit 3
python skills/houdini-agent/tools/query.py search "烟不显示" --kind recipe --limit 3
python skills/houdini-agent/tools/query.py search "工具超时" --max-chars 6000
python skills/houdini-agent/tools/query.py show recipe-cloth-penetration
python skills/houdini-agent/tools/query.py sources S-VELLUMTIPS
```

输出 JSON，包含 Wiki 路径、Skill、建议第一步、验收条件、来源、覆盖等级。检索为中英文关键词/中文二元切分的加权排序，**不是向量库，也不冒充 LLM 语义理解**；不需要 API key 或联网。`--max-chars` 限制字符数，不声称精确 token 数。

安装后，将上述路径前缀换成目标项目的 `.agents/skills/houdini-agent`。返回的 `wiki/...` 路径始终相对该 Skill 根目录。

## 与 CLI 的分工

```text
用户目标
  → houdini-agent（检索、路线、验收计划）
  → 领域 Skill / Wiki / recipe（只读当前需要的资料）
  → houdini-cli tools list + tools inspect（现场调用契约）
  → 专用 MCP 工具；缺能力时才用经过审查的 HOM
  → 数据、缓存、渲染、目标端证据
  → 接受 / 修正 / 明确未验证
```

本包没有新增 `houdini-cli wiki`、`houdini-cli render` 等子命令。查询与安装是独立 Python 工具。真实 CLI 操作与 PowerShell UTF-8 示例见 [快速上手](skills/houdini-agent/wiki/quickstart.md)。

## 维护与许可

`index/topics.json` 和 `index/recipes.json` 保存结构化知识；Wiki 是它们的可阅读视图。`sources.lock.json` 保存资料身份，Git 源固定 commit；滚动网页没有内容快照/hash，不能据名字“lock”误认为不可变镜像。

原创代码和归纳文本按 [MIT](LICENSE) 分发；第三方资料仍归各权利人，本包不包含第三方 HIP、视频、付费课程、字体或文档整站副本。参阅 [第三方说明](THIRD_PARTY_NOTICES.md)。
