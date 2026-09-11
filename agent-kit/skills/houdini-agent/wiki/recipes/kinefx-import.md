# 角色导入后的骨架与 rest 验收

ID: `recipe-kinefx-import` · Skill: `houdini-character` · **recipe-design-not-runtime-tested**

## 输入
关节名/父子关系、rest pose、动画pose、捕获权重、单位/轴、动画时间范围。

## 最小网络意图
`Character import → Skeleton inspection → Rest/pose checks → Bone Deform`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
单位、关节name、父子关系、rest、权重、FPS

## 执行
1. 读取骨架和权重，不先修饰动作。
2. 验证静态rest下几何不异常变形。
3. 用几个极限pose检查局部变换和权重。

## 验收
- name/父子关系与输入说明一致。
- 静态和关键pose通过，再继续完整动画。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../17-kinefx.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-CHAR · Character / KineFX / APEX](https://www.sidefx.com/docs/houdini/character/index.html)
- [C-KINEFX · Houdini KineFX](https://tokeru.com/cgwiki/HoudiniKinefx.html)
