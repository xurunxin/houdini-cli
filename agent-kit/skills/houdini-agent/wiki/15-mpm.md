# MPM、颗粒与其他材料求解器选择

ID: `mpm` · 领域: SOP / DOP · Skill: `houdini-mpm`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
按材料行为和现有版本选方法，不把所有颗粒都归为同一求解器。

## 输入契约
材料目标（雪/沙/弹塑性等）、分辨率、尺度、碰撞、设备资源与当前安装能力。

## 推荐操作
1. 先在当前Houdini确认MPM节点及材料选项，查看安装版本的设备要求；不从显卡品牌推断可运行。
2. 用小体积、简单碰撞、短时段测试材料压缩、流动与回弹。MPM连续体材料设置与Vellum颗粒约束不是可互换参数。
3. 先确定物理行为，再放大域/采样。碎片刚性可转RBD，布与绳通常转Vellum；复杂实体应另查FEM/肌肉工作流。
4. 公开社区小案例用于选题和比较，不宣称视频参数已经提取或场景已经复现。

## 验收条件
- 记录采用MPM而不是替代方案的理由与版本。
- 简单测试证实目标材料趋势，碰撞和边界正常。
- 实际资源开销已测量后再扩大量级。

## 症状 → 优先检查
**节点缺失**：查Houdini版本/安装/授权与类型列表，不创建猜测名称。
**形状过硬或像水**：检查材料模型、单位、初始密度与采样，不只调速度。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`MPM Source`、`MPM Solver`、`Vellum Grains`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-MPM · MPM](https://www.sidefx.com/docs/houdini/mpm/index.html) — index；
- [S-VELLUM · Vellum](https://www.sidefx.com/docs/houdini/vellum/index.html) — index；
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html) — index；
- [E-MPM · Entagma: Smol MPM / Falling Snow](https://entagma.com/smol-mpm-falling-snow/) — landing-only；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
