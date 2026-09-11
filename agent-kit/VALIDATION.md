# 验收记录与明确边界

整理日期：2026-09-11。知识包版本：0.1.0。下述检查针对本包，不借用上游的验收记录冒充本包结果。

## 已完成的离线验证

v0.1 的 64 项 Python unittest 已通过，覆盖中英文检索、受限长度 JSON、真实 schema 字段约束、代码参数封装、CLI/MCP/业务层错误解析、序列文件范围和证据清单检查，以及安装预检、冲突保护、备份、路径隔离、幂等与原 Skill 保留。

v0.1 自动化检查详情保存在 `validation/`。离线测试不启动 Houdini；测试使用临时目录、伪造的 MCP 返回值和最小数据，不会修改用户项目。实际知识包的安装检查也只写临时项目。

结构验证器检查所有 JSON、Skill 元数据、本地 Markdown 链接、topic/recipe 的步骤与验收同步、来源 ID、Git commit 格式、示例边界标识和 Python AST。v0.1 的 11 项 Chromium 阅读器检查已通过，覆盖加载、中文检索、页内导航、20 个 Skill 的筛选、无匹配状态、桌面/移动宽度溢出和无外部请求/无 JavaScript 错误。当前环境限制 file URL 导航，测试通过 set_content 注入同一份完整 HTML；未把该测试冒充所有用户浏览器的文件协议兼容测试。桌面和移动截图也已人工查看。

## 尚未完成的现场验收

当前构建环境无 Houdini / hython，因此没有执行 HOM API、创建真实 SOP 网络、编译 VEX、模拟 Vellum/Pyro/FLIP/MPM、渲染 Karma，或读回真实 HIP/USD/几何缓存。示例中的参数与 API 路线来自已核对文档，但仍须在目标版本运行后才可升级验证状态。

安装逻辑在 Linux / Python 环境完成离线测试。Windows PowerShell、Houdini 许可证类型、GUI/无界面环境、GPU 及驱动兼容需要各自现场验证；没有将 Linux 测试冒充 Windows 验收。

按 [现场测试矩阵](skills/houdini-agent/wiki/target-smoke.md) 推进。示例默认保守：写场景和触发 cook 需要配置授权；不会保存、清空、删除场景或直接发起全序列渲染。配置授权不能取代真实用户许可。

## 与现有 CLI 的验证边界

本包核对的 `houdini-cli` 为 0.2.0，固定 commit `57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9`；固定上游为 `de4fd93acc207fc57c02b330d421461f5963a945`。

原仓库验收记录是 Windows / Houdini 22.0.368 的只读场景查询和任务会话行为；原记录明确未验收场景编辑、渲染、OPUS、其他版本/许可证及 macOS/Linux。官方在线索引本次显示 22.0.437，不能认为它与用户本机完全相同。来源和核对深度记录在 [来源目录](skills/houdini-agent/wiki/sources.md) 与 [来源注册表](skills/houdini-agent/sources.lock.json)。

独立交付 v0.1 时未修改 GitHub 仓库。此次 PR 仅新增 `agent-kit/` 并补充根 README 的知识包入口；不修改 CLI 实现、已有 Skill、固定 MCP 配置或 Houdini 场景，也不直接更新主分支。安装过程只在临时目录中验证，未访问用户机器上的项目。

## 成功等级不能混淆

CLI 进程退出成功 ≠ MCP 工具成功 ≠ 业务结果完整 ≠ 节点输出正确 ≠ 动画稳定 ≠ 视觉达标。

`inspect_result.py` 只检查已识别返回结构；未知结构返回 unknown。`validate_sequence.py` 只检查文件序列结构，不解码图像、不确认内容新鲜度。`check_acceptance.py` 只检查证据清单结构和文件存在，不评判视觉，也不证明证据真实表达了描述。所有工具均保留这些边界。

## 复核命令

```bash
python tools/rebuild_wiki.py --check
python tools/validate_kit.py .
python -m unittest discover -s tests -v
python tools/build_site.py
```

如更新了 canonical JSON，应先执行不带 `--check` 的重建，再做同步验证。来源站点内容是滚动的，离线结构验证不会再次访问外网。

## PR 集成复核（2026-09-11）

此次集成重新运行 Python 离线测试、生成同步检查、结构/本地链接检查、HTML 重建和临时项目安装查询。结果分别记录在 `validation/pr-unittest.txt`、`validation/pr-generated-sync.json`、`validation/pr-structure.json` 和 `validation/pr-install-smoke.json`。

原始 `validation/browser.json` 是 v0.1 阅读器的历史验收；本次未重新执行浏览器或 Houdini 现场测试。离线 HTML 从同一构建器重建，未修改浏览器代码。集成过程保留原始来源、配方和示例验证等级。
