# RBD / Bullet：碎裂、约束、代理与回传

ID: `rbd` · 领域: SOP / DOP · Skill: `houdini-rbd`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
用碎片身份和约束网络管理破坏，不靠碎裂外观判断模拟正确。

## 输入契约
带稳定name的碎片、packed几何、碰撞代理、约束几何与属性、驱动/静态物体。

## 推荐操作
1. 先完成可识别的piece分割与name；render geometry和proxy关系明确，避免高模直接承担所有碰撞成本。
2. 按当前RBD Bullet Solver输入标签接geometry、constraints、proxy等；不同版本的输入顺序不能从记忆猜。
3. 在不加次级碎屑前测试碰撞形状、初始重叠、质量、active/animated状态。约束阈值需结合尺度和加载方式。
4. 确认破裂时刻和大块运动后再提高约束细节与碎屑。高模回传用稳定piece映射，并检查未模拟部分。

## 验收条件
- piece name映射无缺失/重复，约束端点能找到实体。
- 静止测试无初始爆炸，受力与破裂顺序合理。
- 渲染输出与代理运动一致，缓存可完整回放。

## 症状 → 优先检查
**第一帧炸开**：检查初始重叠、碰撞padding、代理精度、约束长度和尺度。
**碎片全部粘死**：检查约束类型/强度、active和animated驱动。
**高模错位**：查name映射与packed变换，避免重复应用。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`RBD Material Fracture`、`RBD Configure`、`RBD Constraints From Rules`、`RBD Bullet Solver`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-RBD · Destruction](https://www.sidefx.com/docs/houdini/destruction/index.html) — index；
- [S-BULLET · RBD Bullet Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/rbdbulletsolver.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
