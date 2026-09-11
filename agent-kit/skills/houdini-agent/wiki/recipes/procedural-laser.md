# 反射/折射光路线的学习与原型入口

ID: `recipe-procedural-laser` · Skill: `houdini-vex` · **recipe-design-not-runtime-tested**

## 输入
Run Over、输入编号、每个输入的属性与坐标空间、必要的 spare parameters、是否有时间反馈。

## 最小网络意图
`Ray origin/direction → Intersection iteration → Curve segments → Shading`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
表面法线、介质、迭代上限、碰撞epsilon、出射规则

## 执行
1. 先读官方相交/方向计算函数与作者案例公开介绍；当前未复现Entagma视频内部网络。
2. 用一个平面或简单玻璃体做几何路线测试，显式限制反弹次数。
3. 将几何光路线与真正物理渲染效果区分，不把可视化曲线当完整光学求解。

## 验收
- 最小几何下反射方向可校验。
- 没有无限循环/零长度段，说明物理简化范围。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../07-vex.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-VEX · VEX snippets](https://www.sidefx.com/docs/houdini/vex/snippets.html)
- [C-VEX · Houdini VEX](https://tokeru.com/cgwiki/HoudiniVex1.html)
- [C-CHEAT · VEX cheat sheet](https://tokeru.com/cgwiki/VexCheatSheet.html)
- [C-JOY · Joy of VEX](https://tokeru.com/cgwiki/JoyOfVex.html)
- [J-VEX · John Kunz VEX Wrangle Snippets](https://wiki.johnkunz.com/index.php?title=VEX_Wrangle_Snippets)
- [E-LASER · Entagma: Procedural Refracting / Reflecting Lasers](https://entagma.com/procedural-refracting-reflecting-lasers/)
