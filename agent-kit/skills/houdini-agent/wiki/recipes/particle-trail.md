# 按稳定 id 生成粒子轨迹

ID: `recipe-particle-trail` · Skill: `houdini-particles` · **recipe-design-not-runtime-tested**

## 输入
发射位置/面、发射速率、初速度、id、age/life、碰撞对象、帧范围。

## 最小网络意图
`POP with stable id → Cache → Trail/connect by id → Sweep`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
id、长度窗口、采样步长、曲线连接方式

## 执行
1. 先验证出生/死亡期间id不重用或冲突。
2. 缓存必要id和P，再按id重建对应轨迹；不要按ptnum连线。
3. 轨迹网格化与模拟分离，用同一缓存比较宽度/采样。

## 验收
- 新旧粒子不会被错误连成一条曲线。
- 连续播放时轨迹长度与时间窗口一致。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../10-particles.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-POP · Particles](https://www.sidefx.com/docs/houdini/dopparticles/index.html)
- [C-SOLVER · The Solver SOP](https://tokeru.com/cgwiki/The_solver_sop.html)
- [J-ATTR · John Kunz VEX Attribute Glossary](https://wiki.johnkunz.com/index.php?title=VEX_Attribute_Glossary)
