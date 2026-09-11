# Agent 输出交付前的证据审查

ID: `recipe-review-delivery` · Skill: `houdini-debug` · **recipe-design-not-runtime-tested**

## 输入
原始brief、参考图/效果、限制、目标节点和输出路径、实际版本、评估帧段。

## 最小网络意图
`Brief → Technical outputs → Temporal review → Visual review → Report`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
证据路径、实际版本、检查范围、结果等级

## 执行
1. 按acceptance模板逐项填pass/fail/unknown，不提前填通过。
2. 所有pass连接到实际文件、日志、图像或帧段。
3. 对未运行/未观看部分说明下一项最低成本验证。

## 验收
- 报告没有把脚本编译当Houdini通过。
- 每个通过项有证据，未覆盖范围明确。

风险: `inspection`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../31-acceptance.md) · [执行协议](../02-cli-contract.md)

## 来源
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md)
- [S-GEO · hou.Geometry](https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html)
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html)
