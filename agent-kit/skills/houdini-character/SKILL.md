---
name: houdini-character
description: Houdini KineFX、APEX、crowds、毛发羽毛肌肉的角色数据与能力定位。
---

# houdini-character

## 按需资料

依赖同目录安装的 `houdini-agent` 知识目录；直接使用本技能，无需先加载总路由。
只读与问题相关的卡片；已有准确入口时无需再检索。查询或写方案不启动 Houdini。

- [按需阅读：KineFX：骨架、重定向与变形数据](../houdini-agent/wiki/17-kinefx.md)
- [按需阅读：APEX：角色图与动画系统入口](../houdini-agent/wiki/18-apex.md)
- [按需阅读：Crowds：Agent、状态与动作混合](../houdini-agent/wiki/19-crowds.md)
- [按需阅读：毛发、羽毛与肌肉工作流导航](../houdini-agent/wiki/20-groom.md)

## 数据与取舍

- 输入契约：关节名/父子关系、rest pose、动画pose、捕获权重、单位/轴、动画时间范围。
- 导入后先检查关节层级、name唯一性、rest与animated数据的职责。不要先用Rig Pose掩盖坐标错误。
- 动画通过后再打包成可复用资产或交给APEX控制层。导出前在接收端重验骨架与曲线。

## 现场执行

实际操作按 [CLI 契约](../houdini-agent/wiki/02-cli-contract.md) 执行；环境未变时复用已核对的 schema 与节点信息。保留无关现场，在授权命名空间内串行修改、读回并修复到结果通过；超时未知操作先查状态，不重放。

## 执行任务完成条件

- 静止pose保持模型、关键关节方向正确。
- 极限姿态下权重、关节缩放和变形可接受。
- 动画帧率/范围/根运动符合交付约定。

## 定位失败

- 角色爆炸：检查rest/animated输入错接、权重与骨架不匹配。
- 重定向脚滑：先核对比例、根运动、时间采样和接触段，不只改脚位置。

## 返回结果

交付所请求的结论、代码或产物；现场操作附改动、路径与证据。标明技术、时间、视觉未验证项，离线检查不代表 Houdini 运行通过；受阻时保留产物和具体阻塞。
