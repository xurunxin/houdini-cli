---
name: houdini-sop
description: Houdini 程序化建模、属性、曲线、UV或复制实例；不用于直接设置动力学求解器。
---

# houdini-sop

## 按需资料

依赖同目录安装的 `houdini-agent` 知识目录；直接使用本技能，无需先加载总路由。
只读与问题相关的卡片；已有准确入口时无需再检索。查询或写方案不启动 Houdini。

- [按需阅读：属性、组与几何数据契约](../houdini-agent/wiki/04-attributes.md)
- [按需阅读：程序化建模、曲线、拓扑与 UV](../houdini-agent/wiki/05-modeling.md)
- [按需阅读：散布、复制、朝向与打包实例](../houdini-agent/wiki/06-instancing.md)

## 数据与取舍

- 输入契约：Geometry Spreadsheet 或 HOM 属性清单；属性 owner、storage、tuple size、含义、空间与有效范围。
- point 是共享位置，vertex 是某个 primitive 对 point 的引用。需要面间不连续的 UV/法线时，先检查是否应在 vertex 上保存。
- 重拓扑、融合、排序后重查 id、name、UV、N。复制/打包后区分外层 packed 属性和内部几何属性。

## 现场执行

实际操作按 [CLI 契约](../houdini-agent/wiki/02-cli-contract.md) 执行；环境未变时复用已核对的 schema 与节点信息。保留无关现场，在授权命名空间内串行修改、读回并修复到结果通过；超时未知操作先查状态，不重放。

## 执行任务完成条件

- 必需属性存在且 owner、类型、tuple size 正确。
- 数值范围、空组、UV接缝和名称唯一性按任务检查。
- 用小样本定位后，对发布所需字段做全量验收或明确抽样范围。

## 定位失败

- 颜色或 UV 断裂/抹平：查 owner 与 Promote 聚合，不靠反复 Smooth 掩盖。
- 随机变化闪烁：ptnum 随拓扑变化，改用经过验证的稳定 id。
- Wrangle 读到零：缺属性可能得到默认值；先 has*attrib 检查，不把零视为真实数据。

## 返回结果

交付所请求的结论、代码或产物；现场操作附改动、路径与证据。标明技术、时间、视觉未验证项，离线检查不代表 Houdini 运行通过；受阻时保留产物和具体阻塞。
