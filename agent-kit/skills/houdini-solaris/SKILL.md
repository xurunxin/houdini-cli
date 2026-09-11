---
name: houdini-solaris
description: Houdini USD/LOP场景组装、层、variant、prim与材质绑定排错。
---

# houdini-solaris

## 按需资料

依赖同目录安装的 `houdini-agent` 知识目录；直接使用本技能，无需先加载总路由。
只读与问题相关的卡片；已有准确入口时无需再检索。查询或写方案不启动 Houdini。

- [按需阅读：Solaris / USD：场景组装、层与绑定](../houdini-agent/wiki/21-solaris.md)

## 数据与取舍

- 输入契约：目标stage、prim paths、资产layer、reference/payload、variant、单位/时间、材质/灯光/相机。
- 确定SOP→USD边界与命名方案，保存稳定prim path；path是USD结构标识，不等于Houdini节点path。
- 导出后在新的受控读回路径检查依赖可解析、prim和绑定一致；不要覆盖原资产。

## 现场执行

实际操作按 [CLI 契约](../houdini-agent/wiki/02-cli-contract.md) 执行；环境未变时复用已核对的 schema 与节点信息。保留无关现场，在授权命名空间内串行修改、读回并修复到结果通过；超时未知操作先查状态，不重放。

## 执行任务完成条件

- 最终stage中prim path、transform、variant与意图相符。
- 材质binding解析到存在的材质，非只看Assign Material节点。
- USD及资产/纹理依赖在交付环境可解析。

## 定位失败

- 材质不生效：检查匹配prim路径、binding层与强度、材质path和渲染delegate。
- 导出后资产消失：检查payload加载、匿名层与相对路径。
- 几何比例错：核对metersPerUnit、轴向和SOP导入变换。

## 返回结果

交付所请求的结论、代码或产物；现场操作附改动、路径与证据。标明技术、时间、视觉未验证项，离线检查不代表 Houdini 运行通过；受阻时保留产物和具体阻塞。
