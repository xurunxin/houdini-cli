# 可重复的 rest 空间噪声形变

ID: `recipe-rest-noise` · Skill: `houdini-vex` · **recipe-design-not-runtime-tested**

## 输入
Run Over、输入编号、每个输入的属性与坐标空间、必要的 spare parameters、是否有时间反馈。

## 最小网络意图
`Rest capture → Point Wrangle → Normal → OUT`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
rest属性、幅度/频率、法线、时间依赖

## 执行
1. 在任何变形前创建稳定rest，不在变形后反复覆盖。
2. 基于rest计算输出P；纯时间函数动画不使用反馈。
3. 对同一帧重复cook确认不继续增长位移。

## 验收
- 同帧同输入结果稳定。
- 幅度、尺度和边界条件没有产生NaN/退化。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../07-vex.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/vex/rest_displacement.vfl)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [S-VEX · VEX snippets](https://www.sidefx.com/docs/houdini/vex/snippets.html)
- [C-VEX · Houdini VEX](https://tokeru.com/cgwiki/HoudiniVex1.html)
- [C-CHEAT · VEX cheat sheet](https://tokeru.com/cgwiki/VexCheatSheet.html)
- [C-JOY · Joy of VEX](https://tokeru.com/cgwiki/JoyOfVex.html)
- [J-VEX · John Kunz VEX Wrangle Snippets](https://wiki.johnkunz.com/index.php?title=VEX_Wrangle_Snippets)
