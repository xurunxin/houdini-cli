---
name: houdini-agent
description: 为使用 houdini-cli 的 Agent 路由 Houdini 建模、VEX、模拟、角色、USD、渲染、Copernicus、PDG 和 HDA 知识。按需查询 Wiki、发现实时节点和参数、生成受控操作并按证据验收；不替代 Houdini 安装、许可证或用户授权。
---

# Houdini Agent：先检索，再发现，再执行

## 最小读取策略
本目录为 `KIT`。首次只读本文件与 [CLI契约](wiki/02-cli-contract.md)。用 `python KIT/tools/query.py search "用户的实际问题" --limit 3 --max-chars 6000` 查询；只打开命中的topic/recipe。不要把所有Wiki、工具schema、几何属性灌入上下文。Python运行文件要用真实绝对路径，不把 `KIT` 当命令变量。

## 路由
几何/属性/复制→houdini-sop；算法→houdini-vex；VDB→houdini-volumes；反馈→houdini-simulation；粒子/刚体/布/烟火/水/材料→对应particles/rbd/vellum/pyro/flip/mpm；地形→terrain；KineFX/APEX/群集/毛羽肌肉→character；USD→solaris；材质和Karma→render；图像→copernicus；信号→chops；批量和缓存→pdg；封装/引擎→hda；异常和验收→debug。
没有安装专用skill时直接阅读本目录topic，全部知识仍可用。能力目录与覆盖等级见 [Wiki首页](wiki/README.md)。

## 执行回路
1. 提取目标、输入、单位/FPS、版本、输出、修改边界和预算。概念方案与真实操作分开。
2. `houdini-cli session status`；协调任务后 `session start <task> --launch-app`。复用现有应用，不抢占别的目标。
3. 任务内 `houdini-cli --session <task> tools list`，调用前 `tools inspect <实际工具名>`。现场schema是调用契约；Wiki候选不是工具保证。
4. 只读场景与类型/参数发现。专用工具优先；缺失能力才用检查过的HOM脚本。输入文件由本机读取后封装到代码，勿假设Agent路径在Houdini主机上可见。
5. 先最小输入、低分辨率、短帧段。记录任务命名空间与已完成操作，按阶段执行，工具调用串行。
6. 检查外层CLI、MCP和业务结果，再验证网络、数据及真实文件。batch不回滚；超时结果未知，先核验，不盲目重放。
7. 使用 [验收卡](wiki/31-acceptance.md) 与 `templates/acceptance.json`，区分技术、时间、视觉通过/失败/未验证。不会仅凭几张静帧声称动画无缺陷。
8. 验收完成后 `session end <task>` 默认保留应用。没有明确必要性不关闭/强杀/清空/覆盖用户现场，不暴露桥接端口。

## 快速工具
`tools/query.py` 离线检索；`tools/make_tool_args.py` 依据保存的实时schema封装脚本，不执行；`tools/inspect_result.py` 识别多层错误，无法判定返回unknown；`tools/validate_sequence.py` 只检查序列文件结构，不评审画面。
`examples/hom` 包含只读probe/反射、显式许可cook检查和独立命名空间SOP小样例；`examples/vex` 是注明前置属性/执行域的原创片段。

## 事实与验证边界
当前知识为2026-09-11选取资料的原创归纳，不是SideFX/CGWiki全量镜像。CLI基线0.2.0；仓库已有验收不等于本包的运行验收。脚本仅离线语法/逻辑测试，需在目标Houdini逐项smoke。来源、阅读深度与版本见 `sources.lock.json`；发现级领域必须继续读匹配版本官方资料后再执行。
