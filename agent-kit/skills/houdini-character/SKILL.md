---
name: houdini-character
description: KineFX、APEX、crowds、毛发羽毛肌肉的角色数据与能力定位。 输出最小可验证方案、必要网络变更和带证据的验收结果。
---

# houdini-character

## 激活与依赖
KineFX、APEX、crowds、毛发羽毛肌肉的角色数据与能力定位。
必须同目录安装 `houdini-agent`。先遵循 [执行协议](../houdini-agent/wiki/02-cli-contract.md)，不替代原有 `houdini-cli` 的环境和生命周期能力。

## 开始前
确认目标、已有节点路径、Houdini版本、输入数据、输出格式及允许修改范围。只有阻塞安全执行的信息才询问；其余列明假设并从低成本原型开始。

## 按需知识
- [按需阅读：KineFX：骨架、重定向与变形数据](../houdini-agent/wiki/17-kinefx.md)
- [按需阅读：APEX：角色图与动画系统入口](../houdini-agent/wiki/18-apex.md)
- [按需阅读：Crowds：Agent、状态与动作混合](../houdini-agent/wiki/19-crowds.md)
- [按需阅读：毛发、羽毛与肌肉工作流导航](../houdini-agent/wiki/20-groom.md)

## 工作顺序
1. 用 `houdini-agent/tools/query.py search` 检索当前问题，只读取命中卡片；读取现场工具schema和节点参数。
2. 检查领域输入：关节名/父子关系、rest pose、动画pose、捕获权重、单位/轴、动画时间范围。
3. 写清数据流和修改计划。导入后先检查关节层级、name唯一性、rest与animated数据的职责。不要先用Rig Pose掩盖坐标错误。
4. 在用户授权范围或任务命名空间做最小试验，串行调用；不重置全场景，不覆盖无关节点。
5. 每阶段检查真实数据再继续。动画通过后再打包成可复用资产或交给APEX控制层。导出前在接收端重验骨架与曲线。
6. 提交证据，记录失败/未验证项，结束会话时默认保留应用。

## 必须验收
- 静止pose保持模型、关键关节方向正确。
- 极限姿态下权重、关节缩放和变形可接受。
- 动画帧率/范围/根运动符合交付约定。

## 失败与降级
- 角色爆炸：检查rest/animated输入错接、权重与骨架不匹配。
- 重定向脚滑：先核对比例、根运动、时间采样和接触段，不只改脚位置。
工具缺失时先确认 schema；专用能力不存在才考虑经检查的 HOM。`guide` 或 `discovery` 文档均不代表现场已经通过运行验收。超时先查状态，不重复提交未知写操作。

## 交付
输出：目标与假设、实际版本、网络/参数改动、缓存/渲染/导出路径、技术与视觉验收证据、未验证项及下一步检查。不得用本地Python语法测试冒充Houdini运行测试。
