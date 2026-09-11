# 将已验证网络封装为可维护 HDA

ID: `recipe-hda-package` · Skill: `houdini-hda` · **recipe-design-not-runtime-tested**

## 输入
输入几何约定、暴露参数、命名空间/版本、外部依赖、Houdini与Engine插件版本、许可证。

## 最小网络意图
`Validated subnet → Controlled parameters → Versioned HDA → Fresh-session test`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
namespace/version、输入契约、参数边界、依赖、定义权限

## 执行
1. 确定稳定输入输出和少量高层参数。
2. 封装为新版本资产，不覆盖未知共享定义。
3. 用新会话测试默认、边界、无输入和依赖缺失情形。

## 验收
- 资产可加载并cook，依赖清单完整。
- 修改输入或参数后输出仍满足契约。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../28-hda-engine.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-ASSETS · Digital assets](https://www.sidefx.com/docs/houdini/assets/index.html)
- [S-ENGINE · Houdini Engine reference](https://www.sidefx.com/docs/houdini/ref/hengine.html)
- [S-LABS · SideFX Labs](https://www.sidefx.com/products/sidefx-labs/)
- [C-HDA · Houdini HDA](https://tokeru.com/cgwiki/HoudiniHDA.html)
