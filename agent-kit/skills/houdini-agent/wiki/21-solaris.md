# Solaris / USD：场景组装、层与绑定

ID: `solaris` · 领域: LOP / USD · Skill: `houdini-solaris`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
管理USD组合后的场景，而不是只检查Houdini节点是否存在。

## 输入契约
目标stage、prim paths、资产layer、reference/payload、variant、单位/时间、材质/灯光/相机。

## 推荐操作
1. 确定SOP→USD边界与命名方案，保存稳定prim path；path是USD结构标识，不等于Houdini节点path。
2. 先检查stage中资产是否实际存在、payload是否加载、purpose/visibility及variant选择；再处理材质。
3. 修改前明确编辑层与覆盖强度，不为便利把所有层flatten。修改已有资产优先非破坏覆盖。
4. 外部HOM用LopNode.stage()检查，可能触发cook；editableStage()只在合适的Python LOP执行上下文使用，不能把它当通用外部写入口。
5. 导出后在新的受控读回路径检查依赖可解析、prim和绑定一致；不要覆盖原资产。

## 验收条件
- 最终stage中prim path、transform、variant与意图相符。
- 材质binding解析到存在的材质，非只看Assign Material节点。
- USD及资产/纹理依赖在交付环境可解析。

## 症状 → 优先检查
**材质不生效**：检查匹配prim路径、binding层与强度、材质path和渲染delegate。
**导出后资产消失**：检查payload加载、匿名层与相对路径。
**几何比例错**：核对metersPerUnit、轴向和SOP导入变换。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`SOP Import`、`Reference`、`Sublayer`、`Material Library`、`Assign Material`、`USD ROP`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html) — index；
- [S-LOPNODE · hou.LopNode](https://www.sidefx.com/docs/houdini/hom/hou/LopNode.html) — selected-sections；
- [C-LOPS · Houdini LOPs](https://tokeru.com/cgwiki/HoudiniLops.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
