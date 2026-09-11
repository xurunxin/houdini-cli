# 构造可检查的 curl 速度场

ID: `recipe-point-advection` · Skill: `houdini-particles` · **recipe-design-not-runtime-tested**

## 输入
发射位置/面、发射速率、初速度、id、age/life、碰撞对象、帧范围。

## 最小网络意图
`Points → SOP velocity field → POP/appropriate advection → Cache`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
场频率、幅值、每秒单位、积分步骤、边界

## 执行
1. 先只生成v属性并可视化向量，区别静态数据与真正运动。
2. 在适合的求解器中按时间步推进，不同时重复写位置和积分速度。
3. 用小点数检查涡旋尺度和边界，再添加渲染尺度与颜色。

## 验收
- 速度场方向与尺度可视化正常。
- 连续轨迹无明显跳变，发射/死亡策略清晰。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../10-particles.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/vex/curl_velocity.vfl)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [S-POP · Particles](https://www.sidefx.com/docs/houdini/dopparticles/index.html)
- [C-SOLVER · The Solver SOP](https://tokeru.com/cgwiki/The_solver_sop.html)
- [J-ATTR · John Kunz VEX Attribute Glossary](https://wiki.johnkunz.com/index.php?title=VEX_Attribute_Glossary)
- [S-CURL · curlnoise VEX](https://www.sidefx.com/docs/houdini/vex/functions/curlnoise.html)
