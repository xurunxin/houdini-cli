---
name: houdini-render
description: MaterialX、Karma、灯光相机、渲染输出与视觉验收；不凭成功码判好看。 输出最小可验证方案、必要网络变更和带证据的验收结果。
---

# houdini-render

## 激活与依赖
MaterialX、Karma、灯光相机、渲染输出与视觉验收；不凭成功码判好看。
必须同目录安装 `houdini-agent`。先遵循 [执行协议](../houdini-agent/wiki/02-cli-contract.md)，不替代原有 `houdini-cli` 的环境和生命周期能力。

## 开始前
确认目标、已有节点路径、Houdini版本、输入数据、输出格式及允许修改范围。只有阻塞安全执行的信息才询问；其余列明假设并从低成本原型开始。

## 按需知识
- [按需阅读：MaterialX、纹理、颜色空间与Lookdev](../houdini-agent/wiki/22-materials.md)
- [按需阅读：Karma / ROP 渲染与镜头级验收](../houdini-agent/wiki/23-render.md)

## 工作顺序
1. 用 `houdini-agent/tools/query.py search` 检索当前问题，只读取命中卡片；读取现场工具schema和节点参数。
2. 检查领域输入：目标delegate、材质路径、贴图和UDIM、UV/primvars、图像语义与OCIO/view transform。
3. 写清数据流和修改计划。Karma材质优先在匹配的Material Builder中建立，严格MaterialX互操作需求单独标记；传统VEX材质不是XPU通用兼容路径。
4. 在用户授权范围或任务命名空间做最小试验，串行调用；不重置全场景，不覆盖无关节点。
5. 每阶段检查真实数据再继续。记录纹理路径与视图变换，在同曝光/灯光/相机下比较修改，不用同时改环境掩盖材质问题。
6. 提交证据，记录失败/未验证项，结束会话时默认保留应用。

## 必须验收
- 材质节点合法、绑定正确、纹理可解析。
- 数据图没有错误gamma/颜色变换。
- 目标渲染器的测试图和AOV符合任务需求。

## 失败与降级
- 法线方向怪：确认贴图为向量数据、tangent convention与normal处理链。
- XPU和CPU外观不同：查当前功能支持与shader路径，不宣称两引擎全功能等价。
工具缺失时先确认 schema；专用能力不存在才考虑经检查的 HOM。`guide` 或 `discovery` 文档均不代表现场已经通过运行验收。超时先查状态，不重复提交未知写操作。

## 交付
输出：目标与假设、实际版本、网络/参数改动、缓存/渲染/导出路径、技术与视觉验收证据、未验证项及下一步检查。不得用本地Python语法测试冒充Houdini运行测试。
