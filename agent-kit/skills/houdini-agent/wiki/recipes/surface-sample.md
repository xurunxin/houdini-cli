# 把参考曲面的颜色传给目标点

ID: `recipe-surface-sample` · Skill: `houdini-vex` · **recipe-design-not-runtime-tested**

## 输入
Run Over、输入编号、每个输入的属性与坐标空间、必要的 spare parameters、是否有时间反馈。

## 最小网络意图
`Target points + Reference polygons → Point Wrangle → OUT`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
输入0/1、参考Cd归属、空间一致性、距离阈值

## 执行
1. 把目标点和参考面放在相同坐标空间，确认参考Cd是point vector。
2. 使用xyzdist获得primitive索引与局部UVW，再用primuv插值。
3. 记录采样距离并检查过远点；primitive UV不是贴图UV。

## 验收
- 参考空输入被识别，未把默认零值当成功。
- 抽样目标颜色与曲面插值相符，远离参考的数据按策略处理。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../07-vex.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/vex/sample_surface_color.vfl)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [S-VEX · VEX snippets](https://www.sidefx.com/docs/houdini/vex/snippets.html)
- [C-VEX · Houdini VEX](https://tokeru.com/cgwiki/HoudiniVex1.html)
- [C-CHEAT · VEX cheat sheet](https://tokeru.com/cgwiki/VexCheatSheet.html)
- [C-JOY · Joy of VEX](https://tokeru.com/cgwiki/JoyOfVex.html)
- [J-VEX · John Kunz VEX Wrangle Snippets](https://wiki.johnkunz.com/index.php?title=VEX_Wrangle_Snippets)
- [S-XYZDIST · xyzdist VEX](https://www.sidefx.com/docs/houdini/vex/functions/xyzdist.html)
- [S-PRIMUV · primuv VEX](https://www.sidefx.com/docs/houdini/vex/functions/primuv.html)
