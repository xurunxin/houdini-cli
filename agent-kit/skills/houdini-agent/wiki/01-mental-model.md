# 上下文、数据与任务选路

ID: `mental-model` · 领域: OBJ / SOP / DOP / LOP / COP / CHOP / TOP · Skill: `houdini-agent`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
把自然语言效果拆成数据变换，不把所有请求都当成“生成一段 Python”。

## 输入契约
用户要的是静态模型、逐帧几何、模拟状态、USD 场景、图像、通道，还是批量产物；目标应用/版本、帧率、单位和交付格式。

## 推荐操作
1. 建模和逐帧几何处理优先 SOP；需要前一时刻状态才选 Solver/动力学；镜头组装和 USD 交付用 LOP；图像处理用 Copernicus；通道信号用 CHOP；作业依赖与变体用 TOP。
2. 把概念数据流写出来：输入资产 → 几何预处理 → 状态/变形 → 缓存 → 场景组装 → 着色/渲染。只打开与当前步骤相关的卡片。
3. 区分网络上下文与编程语言：VEX/VOP 是某些运算的表达方式，HOM 是管理和检查场景的 Python API；ROP 是输出/渲染算子，不是统一的渲染器名称。
4. 先交最小预览，验证方向后才提高分辨率、粒子数、模拟时长。复杂方案必须说明哪段跨 SOP/USD、哪段有时间状态。

## 验收条件
- 每一步有输入类型、输出节点、帧/单位、资源预算。
- 能够说明为什么不需要或为什么需要模拟。
- 不使用不相关上下文来凑节点；未覆盖功能可通过官方索引继续定位。

## 症状 → 优先检查
**节点能创建但接不上**：检查父网络 childTypeCategory 与每个输入数据语义，不仅检查线是否存在。
**看起来一样却不能交付**：确认需要的是可编辑网络、几何缓存、USD 还是渲染图，预览不代替目标格式。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Geometry`、`DOP Network`、`LOP Network`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html) — index；
- [S-HOM · HOM Python scripting](https://www.sidefx.com/docs/houdini/hom/index.html) — index；
- [C-INDEX · CGWiki 入口](https://tokeru.com/cgwiki/) — index；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
