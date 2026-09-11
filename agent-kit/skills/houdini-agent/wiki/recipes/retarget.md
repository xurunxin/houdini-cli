# 重定向与根运动排错

ID: `recipe-retarget` · Skill: `houdini-character` · **recipe-design-not-runtime-tested**

## 输入
关节名/父子关系、rest pose、动画pose、捕获权重、单位/轴、动画时间范围。

## 最小网络意图
`Source skeleton/animation + Target rest → Mapping → Retarget → Deform`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
骨架对应、比例、根运动、接触段、重采样

## 执行
1. 先对齐rest和关节映射，再接完整动画。
2. 检查根运动、角色比例与FPS，定位滑步是空间还是时间问题。
3. 对接触段密集查看，不仅检查几张关键姿态。

## 验收
- 关键关节对应正确。
- 接触与根运动的结果符合交付需要。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../17-kinefx.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-CHAR · Character / KineFX / APEX](https://www.sidefx.com/docs/houdini/character/index.html)
- [C-KINEFX · Houdini KineFX](https://tokeru.com/cgwiki/HoudiniKinefx.html)
