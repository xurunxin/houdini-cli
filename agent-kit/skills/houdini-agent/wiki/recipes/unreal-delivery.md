# Houdini Engine / Unreal 交付前检查

ID: `recipe-unreal-delivery` · Skill: `houdini-hda` · **recipe-design-not-runtime-tested**

## 输入
输入几何约定、暴露参数、命名空间/版本、外部依赖、Houdini与Engine插件版本、许可证。

## 最小网络意图
`Version/dependency check → HDA cook in target → Bake/output verification`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
插件/Houdini匹配、单位轴、材质、实例、Labs

## 执行
1. 现场核对插件和Houdini支持组合，不给未经核实的版本承诺。
2. 在接收端验证输入修改、cook与bake。
3. 检查尺度、朝向、实例和材质，记录丢失字段。

## 验收
- 目标工程可实际复现，不只本机Houdini成功。
- 依赖与授权边界明确。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../28-hda-engine.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-ASSETS · Digital assets](https://www.sidefx.com/docs/houdini/assets/index.html)
- [S-ENGINE · Houdini Engine reference](https://www.sidefx.com/docs/houdini/ref/hengine.html)
- [S-LABS · SideFX Labs](https://www.sidefx.com/products/sidefx-labs/)
- [C-HDA · Houdini HDA](https://tokeru.com/cgwiki/HoudiniHDA.html)
