# 目标 Houdini 现场测试矩阵

本环境没有Houdini/hython；下列状态全部为**未执行**。先从只读开始，只有前一门通过并具有修改许可时继续。

| 门 | 动作 | 通过证据 | 停止条件 |
| --- | --- | --- | --- |
| H0 | doctor与session status | 版本、许可、依赖、已有任务归属 | 其他目标占用/场景风险不明 |
| H1 | 同任务tools list / inspect / scene info | 请求成功且复用会话；现有应用未被重启 | 无桥接或schema不符 |
| H2 | runtime_probe / discover_node_types | JSON、版本、类型、参数与现场一致 | 代码能力不可用或工具包装未知 |
| H3 | 明确授权的小Box网络 | OUT尺寸与平移正确，无用户网络修改 | cook失败/同名已存在/请求超时 |
| H4 | VEX小点集 | Run Over/属性前提满足，实际编译和数值通过 | validation有错误 |
| H5 | 布/烟/水等每类独立最小例 | 场景/缓存/关键帧段及当前build | 资源超预算/结果不稳定 |
| H6 | 单帧与短序列Karma | 可解码图像、配置、连续时间与视觉检查 | 输出未知/覆盖风险/渲染超时 |
| H7 | 目标格式/Engine读回 | 接收端版本、几何/材质/动画证据 | 依赖丢失或单位不匹配 |

## 记录格式
复制 [任务计划](../templates/task-plan.json) 和 [验收模板](../templates/acceptance.json)。每项pass必须有实际证据路径和观察，unknown不能改成pass来让测试变绿。记录操作前场景、任务名、允许修改路径、CLI/Houdini版本、已发请求、输出版本和未验证范围。

## 超时演练
只在可放弃的测试环境中设计超时用例；不要在真实客户场景里故意让渲染/写操作中断。超时后检查已发请求产生的节点/文件与应用状态，不自动重试。CLI超时、上游超时和Houdini执行结束是不同事件。

## 历史基线不是本包通过证据
仓库报告Windows/Houdini22.0.368的只读场景查询和任务生命周期验收；并明确编辑、渲染和其他平台等未验收。本包不借用该历史记录宣称新能力运行通过。来源：[R-VALID](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md)。
