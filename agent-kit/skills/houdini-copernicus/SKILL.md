---
name: houdini-copernicus
description: Houdini Copernicus图像/纹理处理及旧COPs迁移；音频通道转chops。
---

# houdini-copernicus

## 按需资料

依赖同目录安装的 `houdini-agent` 知识目录；直接使用本技能，无需先加载总路由。
只读与问题相关的卡片；已有准确入口时无需再检索。查询或写方案不启动 Houdini。

- [按需阅读：Copernicus 与旧 COPs：图像和纹理](../houdini-agent/wiki/24-copernicus.md)

## 数据与取舍

- 输入契约：图像/几何输入、层/通道、分辨率、像素/世界空间、颜色与数据语义、目标输出格式。
- 确认当前网络是新Copernicus还是旧COP2；CGWiki旧Cops技巧只迁移思路，不照搬节点/参数。
- 保存后读取实际文件，检查通道、位深、alpha、边缘与平铺；屏幕预览经过view transform不等于原像素。

## 现场执行

实际操作按 [CLI 契约](../houdini-agent/wiki/02-cli-contract.md) 执行；环境未变时复用已核对的 schema 与节点信息。保留无关现场，在授权命名空间内串行修改、读回并修复到结果通过；超时未知操作先查状态，不重放。

## 执行任务完成条件

- 输出尺寸、通道、数据范围、位深/颜色空间符合目标。
- 贴图在目标材质或应用中通过读回测试。
- 没有把旧COP2参数套进新节点。

## 定位失败

- 合成边缘有黑边：检查alpha预乘约定和颜色处理。
- 导出颜色与视口不同：查view transform、文件编码与接收端解释。

## 返回结果

交付所请求的结论、代码或产物；现场操作附改动、路径与证据。标明技术、时间、视觉未验证项，离线检查不代表 Houdini 运行通过；受阻时保留产物和具体阻塞。
