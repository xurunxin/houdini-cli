# 沿曲线生成稳定的管线或线缆

ID: `recipe-tube` · Skill: `houdini-sop` · **recipe-design-not-runtime-tested**

## 输入
尺寸/单位、轮廓、曲线方向、封闭要求、法线/UV、目标面数、是否需要后续变形或体积碰撞。

## 最小网络意图
`Curve → Resample → frame/orientation → Sweep → OUT`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
采样间距、曲线方向、截面/半径、朝向frame、端盖

## 执行
1. 用简单折线建立尺度，查看采样密度是否跟曲率匹配。
2. 先显示局部轴，解决相邻frame突变，再扫掠非圆截面。
3. 增加倒角/UV等细节前检查急弯、端盖和最小半径。

## 验收
- 非圆截面不意外翻转；端点和急弯不严重自交。
- 修改路径后输出仍可用，参数边界可解释。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../05-modeling.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-MODEL · Modeling](https://www.sidefx.com/docs/houdini/model/index.html)
- [S-BOX · Box SOP](https://www.sidefx.com/docs/houdini/nodes/sop/box.html)
- [S-XFORM · Transform SOP](https://www.sidefx.com/docs/houdini/nodes/sop/xform.html)
- [C-ATTR · Points, vertices and primitives](https://tokeru.com/cgwiki/Points_and_Verts_and_Prims.html)
