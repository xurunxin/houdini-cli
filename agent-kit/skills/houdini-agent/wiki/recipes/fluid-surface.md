# FLIP 粒子到时间稳定表面

ID: `recipe-fluid-surface` · Skill: `houdini-flip` · **recipe-design-not-runtime-tested**

## 输入
物理尺度、初始液体/持续源、容器、碰撞、速度、粒子分离度、表面和白水需求。

## 最小网络意图
`Validated particle cache → Particle Fluid Surface → Cleanup → OUT`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
particle radius scale、体素、平滑、粒子属性、时间一致

## 执行
1. 固定同一段粒子缓存，减少模拟变化对表面调参的干扰。
2. 低分辨网格比较轮廓、细薄结构和孔洞。
3. 连续回放检查时间闪烁，不用单帧好看代替动画通过。

## 验收
- 粒子和表面大形一致。
- 薄流、液滴和表面细节取舍符合镜头预算。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../14-flip.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-FLIP · Fluid simulation](https://www.sidefx.com/docs/houdini/fluid/index.html)
- [S-FLIPMIN · Minimal SOP FLIP setup](https://www.sidefx.com/docs/houdini/fluid/sopminimalsetup.html)
