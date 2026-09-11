# 科技数据流与网络路径动画

ID: `recipe-data-lines` · Skill: `houdini-sop` · **recipe-design-not-runtime-tested**

## 输入
尺寸/单位、轮廓、曲线方向、封闭要求、法线/UV、目标面数、是否需要后续变形或体积碰撞。

## 最小网络意图
`Anchor points → Curves → Resample/frame → Progress/instances → Render`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
路径层级、进度、方向、宽度、实例亮度

## 执行
1. 先确认信息表达和主次路径，不用真实粒子模拟替代可控运动。
2. 沿路径参数驱动亮点或线段进度，稳定采样和朝向。
3. 增加渲染包装前检查拥挤区域和可读性。

## 验收
- 主次关系在目标镜头尺寸下可识别。
- 路径连接正确，速度和节奏有可控参数。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../05-modeling.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-MODEL · Modeling](https://www.sidefx.com/docs/houdini/model/index.html)
- [S-BOX · Box SOP](https://www.sidefx.com/docs/houdini/nodes/sop/box.html)
- [S-XFORM · Transform SOP](https://www.sidefx.com/docs/houdini/nodes/sop/xform.html)
- [C-ATTR · Points, vertices and primitives](https://tokeru.com/cgwiki/Points_and_Verts_and_Prims.html)
