# Astra 技能迁移说明

本次依据 OpenAI 于 2026-09-11 发布的 [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) 调整技能入口、按需读取和完成条件。保持 Markdown 技能跨模型使用，不要求 Astra 专用工具或修改模型配置。

## 修改范围

- 原始 `houdini-cli` 单文件技能与 agent-kit 的 20 个技能，共 21 个入口；缩短 description，删除重复的通用交付宣言。
- 专业技能保留领域输入、求解器差异、诊断依据及验收条件；将统一的六步行程改为按问题选择的指导。已知领域可以直接使用，不必先加载总路由。
- 知识查询、代码方案与现场操作分别处理。查询无需启动 Houdini；准确入口无需重复检索；同一环境已核对的 schema 可复用，版本或环境改变时重新发现。
- `agent-kit/AGENTS.md` 按任务指向知识索引、维护说明与验证工具。授权范围内的可逆修改、离线验证及必要修复持续执行到结果可核对。
- 同步 canonical CLI 契约、生成 Wiki 目录及离线 HTML。原 CLI 安装器只复制一个 SKILL.md，因此该入口继续自包含，未增加安装后丢失的外部引用。

按 UTF-8 字节统计（不是模型 token 基准）：21 个 SKILL.md 从 **55,688** 减至 **43,137**，减少约 **22.5%**；全部 description 从 **3,432** 减至 **1,888**，减少约 **45.0%**。领域 Wiki、40 个配方及 HOM/VEX 示例继续按需可用。

## 保留的执行契约

实时工具 schema、内部节点类型与参数仍以目标 Houdini 为准；保持会话归属、桥接串行及 .hip/无关节点保护。batch 不回滚，超时返回未知时先查状态，不重放创建、模拟或渲染。默认释放 MCP 并保留应用；修改/cook 示例的显式开关、文件路径保护和已有预算边界不变。

技术、时间、视觉分别验收；文件存在、成功 JSON 或离线 Python 检查都不等于效果运行通过。未验证的目标保留状态与具体阻塞，不因“持续完成”扩大权限或自动提高预算。

## 行为回归场景

下表为本次逐项核对的指令与现有离线用例覆盖，**不是在 Houdini 上完成的模型效果评测**。

| 请求或输入 | 应有行为 | 本次依据 |
| --- | --- | --- |
| “只解释布料高速碰撞穿透，不启动 Houdini” | 直接读取 Vellum 卡，按厚度、重叠、变形采样及子步分析；不建会话 | 专业入口与 Vellum 排错项人工核对 |
| 已知 SOP 节点只需修改一项属性 | 直接用 SOP 技能与现场契约，复用有效 schema，不安装全套技能或运行无关 smoke | SOP 入口、CLI 技能与 quickstart 人工核对 |
| 创建或渲染超时，外层报告失败 | 状态记为 unknown，先核验已有节点、文件和任务；不直接重放 | CLI 契约；ResultTests 的 unknown、部分成功与内嵌失败用例 |
| 布料、烟火、刚体或 USD 任务 | 保留对应输入/数据流和验收依据，不用通用模板替代专业判断 | 19 个专业技能的原领域指导、验收和故障项对照保留 |
| 原型成功但交付帧段还未通过 | 在已有授权与预算内继续修复；无法现场验证时标注未验证 | CLI 完成条件与专业技能结果说明人工核对 |
| 仅安装核心包或安装全套包 | 核心 Wiki 查询可用；全套相对链接可达；未知用户文件不被覆盖 | 现有递归安装、真实检索、冲突/路径保护用例 |
| 清单或序列文件检查通过 | 不宣称编译、动画、听音或视觉评审通过 | AcceptanceTests、SequenceTests 与各技能证据边界 |

## 实际验证

2026-09-11，Linux / Python 3.12.14：

- `python3 agent-kit/tools/rebuild_wiki.py` 生成同步；74 个生成页保持一致。
- `python3 agent-kit/tools/build_site.py` 重建离线 HTML，嵌入 140 个文档。
- 在 `agent-kit` 执行 `python3 tools/validate_kit.py .`：通过，20 个技能、32 个主题、40 个配方、81 条来源、319 条本地链接。
- 在 `agent-kit` 执行 `python3 -m unittest discover -s tests -v`：**77 项通过**，涵盖安装、查询、内容同步、错误解析、参数封装和路径保护。
- `node scripts/check.mjs`：语法和技能检查通过；`git diff --check`：通过。
- 重建后刷新并核验 `agent-kit/MANIFEST.sha256`。

未运行目标 Houdini、VEX 编译、模拟、Karma 渲染或真实音画验收，也未复跑浏览器与 Windows 测试。未把已有来源的 runtime 状态提升为通过。没有修改 CLI 实现、依赖或安装行为；此次收益是入口与流程改进，不能据此宣称 Astra 效果分数已经提升。
