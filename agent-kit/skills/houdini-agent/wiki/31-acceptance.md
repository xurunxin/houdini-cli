# 技术、时间与视觉三层验收

ID: `acceptance` · 领域: ALL · Skill: `houdini-debug`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
让Agent提交可检查的证据，不把执行完成当作创作完成。

## 输入契约
原始brief、参考图/效果、限制、目标节点和输出路径、实际版本、评估帧段。

## 推荐操作
1. 技术层：参数/连接/字段/prim/帧清单可验证；静态脚本编译只验证Python语法，不验证HOM/API或VEX编译。
2. 时间层：连续回放运动、碰撞、发射、断裂等事件窗口；静帧采样只能发现部分问题，报告覆盖范围。
3. 视觉层：对照brief看主体轮廓、比例、层次、材质、光照和情绪；逐项给具体证据，不编造“审美评分99分”。
4. 区分pass/fail/unknown/not_applicable，unknown不算pass。重要输出需要回读与目标端测试。
5. 报告变更、证据路径、未验证项、后续最低成本检查；只总结实际运行过的内容。

## 验收条件
- 每个通过项至少一个可定位的证据。
- 失败和未验证项不混为完成。
- 原场景和用户资产保留策略可解释。

## 症状 → 优先检查
**工具报告成功但任务未达成**：回到brief和实际输出逐项评估。
**只有几张截图**：明确时间验收不足；补连续片段而非夸大截图结论。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Evidence manifest`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md) — file；
- [S-GEO · hou.Geometry](https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html) — selected-sections；
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html) — index；
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
