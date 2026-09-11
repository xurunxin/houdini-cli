# 音频或信号驱动几何参数

ID: `recipe-audio-drive` · Skill: `houdini-chops` · **recipe-design-not-runtime-tested**

## 输入
输入采样率、时间范围、通道名、幅值范围、延迟预算、目标参数/几何绑定。

## 最小网络意图
`Audio/signal → CHOP analysis/filter → Map channels → Parm/geometry`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
采样率、起点、范围、滤波延迟、通道命名

## 执行
1. 先检查实际波形/听音和采样时间，不依赖文件名判断内容。
2. 规范幅值并限制映射范围，记录滤波引入的延迟。
3. 用事件附近连续回放验证图像与音频对齐。

## 验收
- 音画事件对齐有可定位证据。
- 不会把幅值驱动等同于音乐情绪理解。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../25-chops.md) · [执行协议](../02-cli-contract.md)

## 来源
- [C-CHOPS · Houdini CHOPs](https://tokeru.com/cgwiki/HoudiniChops.html)
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html)
