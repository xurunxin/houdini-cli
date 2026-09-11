---
name: houdini-sop
description: 程序化建模、属性、曲线、UV或复制实例；不用于直接设置动力学求解器。 输出最小可验证方案、必要网络变更和带证据的验收结果。
---

# houdini-sop

## 激活与依赖
程序化建模、属性、曲线、UV或复制实例；不用于直接设置动力学求解器。
必须同目录安装 `houdini-agent`。先遵循 [执行协议](../houdini-agent/wiki/02-cli-contract.md)，不替代原有 `houdini-cli` 的环境和生命周期能力。

## 开始前
确认目标、已有节点路径、Houdini版本、输入数据、输出格式及允许修改范围。只有阻塞安全执行的信息才询问；其余列明假设并从低成本原型开始。

## 按需知识
- [按需阅读：属性、组与几何数据契约](../houdini-agent/wiki/04-attributes.md)
- [按需阅读：程序化建模、曲线、拓扑与 UV](../houdini-agent/wiki/05-modeling.md)
- [按需阅读：散布、复制、朝向与打包实例](../houdini-agent/wiki/06-instancing.md)

## 工作顺序
1. 用 `houdini-agent/tools/query.py search` 检索当前问题，只读取命中卡片；读取现场工具schema和节点参数。
2. 检查领域输入：Geometry Spreadsheet 或 HOM 属性清单；属性 owner、storage、tuple size、含义、空间与有效范围。
3. 写清数据流和修改计划。point 是共享位置，vertex 是某个 primitive 对 point 的引用。需要面间不连续的 UV/法线时，先检查是否应在 vertex 上保存。
4. 在用户授权范围或任务命名空间做最小试验，串行调用；不重置全场景，不覆盖无关节点。
5. 每阶段检查真实数据再继续。重拓扑、融合、排序后重查 id、name、UV、N。复制/打包后区分外层 packed 属性和内部几何属性。
6. 提交证据，记录失败/未验证项，结束会话时默认保留应用。

## 必须验收
- 必需属性存在且 owner、类型、tuple size 正确。
- 数值范围、空组、UV接缝和名称唯一性按任务检查。
- 用小样本定位后，对发布所需字段做全量验收或明确抽样范围。

## 失败与降级
- 颜色或 UV 断裂/抹平：查 owner 与 Promote 聚合，不靠反复 Smooth 掩盖。
- 随机变化闪烁：ptnum 随拓扑变化，改用经过验证的稳定 id。
- Wrangle 读到零：缺属性可能得到默认值；先 has*attrib 检查，不把零视为真实数据。
工具缺失时先确认 schema；专用能力不存在才考虑经检查的 HOM。`guide` 或 `discovery` 文档均不代表现场已经通过运行验收。超时先查状态，不重复提交未知写操作。

## 交付
输出：目标与假设、实际版本、网络/参数改动、缓存/渲染/导出路径、技术与视觉验收证据、未验证项及下一步检查。不得用本地Python语法测试冒充Houdini运行测试。
