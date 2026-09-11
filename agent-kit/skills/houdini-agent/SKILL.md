---
name: houdini-agent
description: 查询 Houdini Wiki、选择领域技能并协调跨领域场景任务；已明确领域时直接使用对应专业技能。
---

# Houdini Agent

## 查询与选路

本目录记为 `KIT`。已有专业技能或知识卡时直接使用；仅领域不明、跨领域或未装专业技能时由本入口路由。只要知识/代码方案就离线完成，不启动应用或收集无关运行参数。

按问题运行 `python KIT/tools/query.py search "用户的实际问题" --limit 3 --max-chars 6000`，只打开命中的 topic/recipe。把 `KIT` 替换为真实路径；运行 Python 文件时使用绝对路径。覆盖等级见 [Wiki 目录](wiki/README.md)，不预载全库或全部 schema。

| 目标 | 专业技能 |
| --- | --- |
| 几何、属性、复制 / VEX算法 / VDB | houdini-sop / houdini-vex / houdini-volumes |
| 时间状态与求解器选型 | houdini-simulation |
| 粒子、刚体、布绳、烟火、水、材料 | houdini-particles / houdini-rbd / houdini-vellum / houdini-pyro / houdini-flip / houdini-mpm |
| 地形 / KineFX、APEX、群集、毛羽肌肉 | houdini-terrain / houdini-character |
| USD组装 / MaterialX、Karma、灯光相机 | houdini-solaris / houdini-render |
| 图像 / 动画与音频信号 | houdini-copernicus / houdini-chops |
| 批量、缓存 / HDA、Engine交付 / 异常诊断 | houdini-pdg / houdini-hda / houdini-debug |

未装专业技能时，命中的本目录知识卡仍可直接使用，不要求为当前任务安装全套技能。

## 需要现场操作时

读取 [CLI 契约](wiki/02-cli-contract.md)；需要确认节点类型、输入或参数时读 [运行时发现](wiki/03-runtime-discovery.md)。先复用当前任务和用户现场，再依据实时 schema 串行操作；同一环境已核对的信息无需反复发现。

专用工具优先；能力缺失才使用检查过的 HOM。`tools/make_tool_args.py` 将本机脚本嵌入参数，不假设 Agent 路径在 Houdini 主机可见。HOM 例子与 VEX 片段的输入、cook/修改开关和执行域见 [示例前提](examples/README.md)。

在现有授权、输出路径和预算内完成请求的修改与验证；已授权的可逆修复不逐步重新确认。batch 不回滚，超时结果未知，先核验节点/文件/任务状态，再决定后续动作。不得抢占其他目标会话、清空或覆盖无关现场。

## 完成与证据

查询交付可用结论和对应知识来源；实现任务持续到请求产物及相关检查通过，或有明确环境、权限或预算阻塞。记录实际版本、改动和产物路径；按 [验收卡](wiki/31-acceptance.md) 区分技术、时间、视觉结果。模板 `templates/acceptance.json` 适用于正式验收，不要求简单查询填表。

`tools/inspect_result.py` 识别多层错误，无法判定返回 unknown；`tools/validate_sequence.py` 只检查序列文件结构。成功码或几张静帧不能证明动画、声音或视觉质量通过。目标验收后按 CLI 契约释放任务 MCP，默认保留应用。

本包为 2026-09-11 选取资料的原创归纳；CLI 知识基线 0.2.0。来源与阅读深度见 `sources.lock.json`；发现级领域执行前需继续读匹配版本官方资料。离线测试不证明目标 Houdini 的节点、VEX、模拟或渲染已运行通过。
