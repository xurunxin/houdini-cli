# CHOP：动画通道、信号和音频驱动

ID: `chops` · 领域: CHOP · Skill: `houdini-chops`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
将信号采样与动画帧分开，提供可回放的参数驱动。

## 输入契约
输入采样率、时间范围、通道名、幅值范围、延迟预算、目标参数/几何绑定。

## 推荐操作
1. 检查CHOP采样率与Houdini FPS及起始时间的对应，不能用样本索引直接当帧。
2. 先归一化并观察通道，再选择滤波、lag或映射；滤波可能引入延迟，需在事件附近对齐检验。
3. 输出/导出到目标参数时确认通道名和覆盖关系。音频幅值只能驱动数值，不证明音乐情绪或剪辑合适。
4. 检测或合成的节拍候选需要听音/波形和时间校验，不将文件名/标签替代实际音频判断。

## 验收条件
- 采样率、时间对齐与通道映射正确。
- 连续播放无多余抖动或不可接受延迟。
- 音频相关主张有实际听音/信号证据或明确未验证。

## 症状 → 优先检查
**驱动总是晚一拍**：检查重采样、起点和滤波延迟。
**表达式不工作**：区分CHOP通道、SOP属性与参数表达式上下文。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`File CHOP`、`Math CHOP`、`Filter CHOP`、`Lag CHOP`、`Channel SOP`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [C-CHOPS · Houdini CHOPs](https://tokeru.com/cgwiki/HoudiniChops.html) — selected-sections；
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html) — index；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
