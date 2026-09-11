# 受控的短时爆发烟火原型

ID: `recipe-pyro-burst` · Skill: `houdini-pyro` · **recipe-design-not-runtime-tested**

## 输入
源几何与持续时间、字段名/类型、体素尺寸、域/边界、碰撞、散热和外观需求。

## 最小网络意图
`Timed source → Fields → Sparse Pyro → Cache → Volume shading`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
注入持续时间、体素、域边界、上升/扩散、扰动

## 执行
1. 先确定源的短时窗口和主运动，不在每帧重复无意注入。
2. 粗分辨率验证爆发形状与域边界。
3. 主要轮廓认可后加细节并独立进行发光/密度lookdev。

## 验收
- 源关闭后演变正确，域不裁切关键形状。
- 模拟与渲染参数修改可分别追踪。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../13-pyro.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-PYRO · Pyro](https://www.sidefx.com/docs/houdini/pyro/index.html)
- [S-PYROSOLVER · Pyro Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/pyrosolver.html)
- [S-PYROLOOK · Pyro workflow/lookdev](https://www.sidefx.com/docs/houdini/pyro/lookdev.html)
- [C-PYRO · Smoke and Pyro (mixed/legacy)](https://tokeru.com/cgwiki/Smoke_and_Pyro.html)
