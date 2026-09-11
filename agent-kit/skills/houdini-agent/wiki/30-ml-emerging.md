# ML、Gaussian Splats 与新功能检索

ID: `ml-emerging` · 领域: SOP / LOP · Skill: `houdini-agent`
覆盖等级: **discovery** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
发现新能力并建立验证入口，不将索引覆盖宣称为已经复现。

## 输入契约
目标功能、安装版本/设备、模型或数据来源与授权、预处理、预期输出、可复现小样本。

## 推荐操作
1. 从目标版本官方ML或新功能索引定位节点，再查询现场类型/schema；不凭功能名称猜命令或模型兼容性。
2. 固定输入样本、模型版本与预处理，先验证输出shape/语义和性能。外部模型/脚本需审查，不自动下载执行。
3. GSplat与普通点云/网格的表示和可重照明能力要单独查目标渲染器限制。
4. 完成真实小样本运行后才将本卡从发现级扩展为正式recipe，并附版本和产物证据。

## 验收条件
- 可定位准确官方页面及实际安装类型。
- 测试数据、模型与结果来源明确。
- 未运行部分保持discovery/未验收标记。

## 症状 → 优先检查
**名称存在但能力不符**：核对版本和数据表示，拒绝用普通点渲染替代GSplat而不说明。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`ML nodes`、`Bake GSplat`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-ML · Machine learning](https://www.sidefx.com/docs/houdini/ml/index.html) — index；
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html) — selected-sections；
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html) — index；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
