# POP 粒子、属性生命周期与轨迹

ID: `particles` · 领域: SOP / DOP · Skill: `houdini-particles`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
构造可控发射、受力、碰撞和生命周期，再交给复制或渲染。

## 输入契约
发射位置/面、发射速率、初速度、id、age/life、碰撞对象、帧范围。

## 推荐操作
1. 先用少量粒子确认发射方向、速率和持续时间。birth时初始化的属性不要每帧被覆盖。
2. 区分直接写位置、写速度、施加力；按目标采用积分一致的方式。不要用每帧随机位置伪装稳定力场。
3. 碰撞预处理与时间采样单独验收，再加湍流和二次细节。Trail/连接轨迹依赖稳定id，不依赖ptnum。
4. 渲染或实例化前确认点尺度、颜色、速度及死粒子处理；预先缓存可视化所需属性。

## 验收条件
- 发射/存活数量、id唯一性、生命周期与目标一致。
- 首中尾连续回放无出生抖动和错误连线。
- 碰撞与轨迹在低分辨率测试中可证实。

## 症状 → 优先检查
**轨迹交叉乱连**：核对id稳定性和按id连接设置。
**粒子变快不受控**：检查速度是否每帧累加、重复力节点和时间步。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`POP Source`、`POP Solver`、`POP Force`、`POP Wrangle`、`Trail`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-POP · Particles](https://www.sidefx.com/docs/houdini/dopparticles/index.html) — index；
- [C-SOLVER · The Solver SOP](https://tokeru.com/cgwiki/The_solver_sop.html) — article；
- [J-ATTR · John Kunz VEX Attribute Glossary](https://wiki.johnkunz.com/index.php?title=VEX_Attribute_Glossary) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
