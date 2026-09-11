# HDA、Labs 与 Houdini Engine / Unreal

ID: `hda-engine` · 领域: SOP / HDA / ENGINE · Skill: `houdini-hda`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
将已经通过验证的网络封装为有输入输出契约的资产。

## 输入契约
输入几何约定、暴露参数、命名空间/版本、外部依赖、Houdini与Engine插件版本、许可证。

## 推荐操作
1. 先在原网络验证默认/边界参数与无输入情形，再提升接口；不要把所有底层参数一股脑暴露。
2. 使用显式namespace/name/version，区分编辑实例和更新定义；不直接覆盖共享HDA定义或解锁用户资产。
3. Labs是附加工具集，记录实际安装版本及依赖。目标机没有Labs时提供依赖说明，不宣称所有labs节点是内置。
4. Engine/Unreal在接收端测试输入、坐标/尺度、材质和bake；支持矩阵以当前SideFX插件资料和安装现场为准。
5. 打包时核对嵌入文件、纹理、缓存、脚本授权；插件升级需要回归，不自动改变项目全局配置。

## 验收条件
- 新会话/接收端可加载并cook。
- 默认、极限、空输入的输出契约明确。
- HDA版本、Labs、插件与许可证要求记录完整。

## 症状 → 优先检查
**本机正常他人失败**：查未打包依赖、Labs版本、绝对路径与资产定义。
**UE方向/尺度不对**：在接收端验证轴向/单位转换与实例变换。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Subnet`、`Digital Asset`、`Labs`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-ASSETS · Digital assets](https://www.sidefx.com/docs/houdini/assets/index.html) — index；
- [S-ENGINE · Houdini Engine reference](https://www.sidefx.com/docs/houdini/ref/hengine.html) — index；
- [S-LABS · SideFX Labs](https://www.sidefx.com/products/sidefx-labs/) — article；
- [C-HDA · Houdini HDA](https://tokeru.com/cgwiki/HoudiniHDA.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
