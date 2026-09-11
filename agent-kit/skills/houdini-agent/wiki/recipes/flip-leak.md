# 液体漏水或流失的诊断

ID: `recipe-flip-leak` · Skill: `houdini-flip` · **recipe-design-not-runtime-tested**

## 输入
物理尺度、初始液体/持续源、容器、碰撞、速度、粒子分离度、表面和白水需求。

## 最小网络意图
`Container/source/collision → FLIP → Particle cache → Surface`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
碰撞SDF、壁厚、边界、粒子分离度、时间步、出口

## 执行
1. 区分设计出口、开域与意外穿透；记录粒子数/体积变化趋势。
2. 检查碰撞体厚度、封闭性与动态变形采样。
3. 验证模拟数据后再看meshing，避免把表面洞误判为液体丢失。

## 验收
- 损失原因定位到源/边界/碰撞或网格化。
- 短时段连续回放无不可接受漏水。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../14-flip.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-FLIP · Fluid simulation](https://www.sidefx.com/docs/houdini/fluid/index.html)
- [S-FLIPMIN · Minimal SOP FLIP setup](https://www.sidefx.com/docs/houdini/fluid/sopminimalsetup.html)
