# KineFX：骨架、重定向与变形数据

ID: `kinefx` · 领域: SOP · Skill: `houdini-character`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
以骨架和蒙皮数据契约解决角色问题，先静态姿态再动画。

## 输入契约
关节名/父子关系、rest pose、动画pose、捕获权重、单位/轴、动画时间范围。

## 推荐操作
1. 导入后先检查关节层级、name唯一性、rest与animated数据的职责。不要先用Rig Pose掩盖坐标错误。
2. 统一单位和轴向；映射源/目标骨架时记录关节对应和比例差异。重定向前验证静态对齐。
3. 用少量关键姿态测试Bone Deform或相应变形链，排查缺权重和局部transform。
4. 动画通过后再打包成可复用资产或交给APEX控制层。导出前在接收端重验骨架与曲线。

## 验收条件
- 静止pose保持模型、关键关节方向正确。
- 极限姿态下权重、关节缩放和变形可接受。
- 动画帧率/范围/根运动符合交付约定。

## 症状 → 优先检查
**角色爆炸**：检查rest/animated输入错接、权重与骨架不匹配。
**重定向脚滑**：先核对比例、根运动、时间采样和接触段，不只改脚位置。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Skeleton`、`Rig Doctor`、`Rig Pose`、`Bone Deform`、`FBX Character Import`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-CHAR · Character / KineFX / APEX](https://www.sidefx.com/docs/houdini/character/index.html) — index；
- [C-KINEFX · Houdini KineFX](https://tokeru.com/cgwiki/HoudiniKinefx.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
