# 诊断、性能与最小复现

ID: `debug-performance` · 领域: ALL · Skill: `houdini-debug`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
先定位失败层和最小复现，避免“重启/重装/加资源”作为第一反应。

## 输入契约
操作时间线、工具JSON、节点错误、版本、资源指标、输入与可复现帧。

## 推荐操作
1. 从CLI/bridge/license→节点创建→参数/连线→cook→数据→渲染/导出逐层排查；各层成功条件不同。
2. 从第一个错误节点向上追依赖，保存当前现场，在副本/任务命名空间做最小输入测试。
3. 量化成本：模拟域/点数/实例/贴图/渲染采样与磁盘I/O；先定位最慢步骤再选缓存、降分辨或并行。
4. 诊断读取geometry/stage也可能cook；限定路径、遍历深度、样本数量和时间预算。不dump全场所有属性。
5. 修复后重跑最小例，再回归相关帧段。无法验证的结果明确unknown，保留日志，不强制全场重cook。

## 验收条件
- 根因或待验证假设有证据和最小复現步骤。
- 修改前后指标可比较，错误未被简单隐藏。
- 没有因排错丢失用户现场或重放未知操作。

## 症状 → 优先检查
**无错误但结果错**：检查数据契约和艺术目标，成功cook不保证语义正确。
**提高超时仍失败**：查上游超时/主线程占用/资源，CLI参数不能消除所有边界。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Performance Monitor`、`Error Nodes`、`Cache`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-HOM · HOM Python scripting](https://www.sidefx.com/docs/houdini/hom/index.html) — index；
- [S-OPNODE · hou.OpNode](https://www.sidefx.com/docs/houdini/hom/hou/OpNode.html) — selected-sections；
- [S-GEO · hou.Geometry](https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html) — selected-sections；
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs) — file；
- [R-SETUP · houdini-cli setup](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/houdini-setup.md) — file；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
