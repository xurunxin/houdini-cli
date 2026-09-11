---
name: houdini-volumes
description: Houdini VDB、SDF、体积转换和字段排错；烟火模拟目标转houdini-pyro。
---

# houdini-volumes

## 按需资料

依赖同目录安装的 `houdini-agent` 知识目录；直接使用本技能，无需先加载总路由。
只读与问题相关的卡片；已有准确入口时无需再检索。查询或写方案不启动 Houdini。

- [按需阅读：Volume / VDB / SDF 数据与运算](../houdini-agent/wiki/08-volumes.md)

## 数据与取舍

- 输入契约：字段名、标量/向量、fog或level set、体素尺寸、transform、active bounds、是否封闭几何。
- 先看字段类型、名称和空间范围。SDF 符号与窄带用途不同于密度，不能把 density 直接当 surface。
- 可视化切片、iso面与数值范围；不要只靠viewport密度滑块判断数据存在。

## 现场执行

实际操作按 [CLI 契约](../houdini-agent/wiki/02-cli-contract.md) 执行；环境未变时复用已核对的 schema 与节点信息。保留无关现场，在授权命名空间内串行修改、读回并修复到结果通过；超时未知操作先查状态，不重放。

## 执行任务完成条件

- 正确字段、类型、transform及active bounds。
- 目标厚度与关键形状在选择的体素尺寸下可表达。
- 渲染路径能读回导出的 VDB 字段。

## 定位失败

- SDF 合并出现裂缝：检查level set窄带和transform，不简单叠加。
- 体积突然吃满内存：检查是否激活了大范围背景/转dense，先缩小域再恢复。

## 返回结果

交付所请求的结论、代码或产物；现场操作附改动、路径与证据。标明技术、时间、视觉未验证项，离线检查不代表 Houdini 运行通过；受阻时保留产物和具体阻塞。
