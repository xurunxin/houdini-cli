---
name: houdini-render
description: Houdini MaterialX、Karma、灯光相机、渲染输出与视觉验收；不凭成功码判好看。
---

# houdini-render

## 按需资料

依赖同目录安装的 `houdini-agent` 知识目录；直接使用本技能，无需先加载总路由。
只读与问题相关的卡片；已有准确入口时无需再检索。查询或写方案不启动 Houdini。

- [按需阅读：MaterialX、纹理、颜色空间与Lookdev](../houdini-agent/wiki/22-materials.md)
- [按需阅读：Karma / ROP 渲染与镜头级验收](../houdini-agent/wiki/23-render.md)

## 数据与取舍

- 输入契约：目标delegate、材质路径、贴图和UDIM、UV/primvars、图像语义与OCIO/view transform。
- Karma材质优先在匹配的Material Builder中建立，严格MaterialX互操作需求单独标记；传统VEX材质不是XPU通用兼容路径。
- 记录纹理路径与视图变换，在同曝光/灯光/相机下比较修改，不用同时改环境掩盖材质问题。

## 现场执行

实际操作按 [CLI 契约](../houdini-agent/wiki/02-cli-contract.md) 执行；环境未变时复用已核对的 schema 与节点信息。保留无关现场，在授权命名空间内串行修改、读回并修复到结果通过；超时未知操作先查状态，不重放。

## 执行任务完成条件

- 材质节点合法、绑定正确、纹理可解析。
- 数据图没有错误gamma/颜色变换。
- 目标渲染器的测试图和AOV符合任务需求。

## 定位失败

- 法线方向怪：确认贴图为向量数据、tangent convention与normal处理链。
- XPU和CPU外观不同：查当前功能支持与shader路径，不宣称两引擎全功能等价。

## 返回结果

交付所请求的结论、代码或产物；现场操作附改动、路径与证据。标明技术、时间、视觉未验证项，离线检查不代表 Houdini 运行通过；受阻时保留产物和具体阻塞。
