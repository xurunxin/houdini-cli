# 在表面散布具有稳定方向和大小的实例

ID: `recipe-scatter` · Skill: `houdini-sop` · **recipe-design-not-runtime-tested**

## 输入
原型的前向轴/原点、目标点位置、稳定 id、N/up 或 orient、缩放策略、原型选择字段。

## 最小网络意图
`Surface → Scatter → id/pscale/orient → Copy to Points → OUT`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
密度、seed、原型轴、实例属性优先级、packed策略

## 执行
1. 选带方向标记的原型并确定前向轴。
2. 建立稳定id再生成随机尺度；表面法线不足以定义全部roll时补up/frame。
3. 先十个实例验证，再扩展到目标密度和渲染表示。

## 验收
- 原型方向、尺寸和分布符合目标。
- 改变帧或重cook不引入无意义随机闪烁。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../06-instancing.md) · [执行协议](../02-cli-contract.md)

[配套示例](../../examples/vex/stable_scale.vfl)：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。

## 来源
- [S-COPY · Copy/instance attributes](https://www.sidefx.com/docs/houdini/copy/instanceattrs.html)
- [C-CHEAT · VEX cheat sheet](https://tokeru.com/cgwiki/VexCheatSheet.html)
- [J-ATTR · John Kunz VEX Attribute Glossary](https://wiki.johnkunz.com/index.php?title=VEX_Attribute_Glossary)
