# PDG / TOPs：批量任务、变体与依赖

ID: `pdg` · 领域: TOP / ROP · Skill: `houdini-pdg`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
将可复现的数据依赖交给任务图，而不是让多个Agent抢同一GUI。

## 输入契约
输入清单、work item属性、依赖、输出文件命名、scheduler、许可证/内存/设备并发预算。

## 推荐操作
1. 先独立完成一个work item，然后扩展wedge。每个变体的输出包含任务/资产/版本/seed，防止路径冲突。
2. 上游生成结果通过声明输出/依赖传递；文件存在不自动证明版本正确，cache策略要与输入指纹关联。
3. 区分in-process与独立hython/Houdini任务；设置资源上限，不能仅按CPU核心数无限启动占许可证的进程。
4. 仅可重复且状态已知的任务允许调度重试。CLI超时未知的GUI写操作不属于安全自动重试对象。

## 验收条件
- 每个item的输入、属性、输出和日志可追踪。
- 一个item失败不会覆盖其他变体的输出。
- 小批次通过后才提高并发，许可证与内存有现场验证。

## 症状 → 优先检查
**输出互相覆盖**：路径缺少wedge/item/版本字段。
**看起来成功但拿到旧缓存**：核对输入指纹和cache命中依据。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Wedge`、`ROP Geometry Output`、`Partition by Attribute`、`Wait for All`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-TOPS · PDG / TOPs](https://www.sidefx.com/docs/houdini/tops/index.html) — index；
- [S-TOPROP · ROP Geometry TOP](https://www.sidefx.com/docs/houdini/nodes/top/ropgeometry.html) — selected-sections；
- [C-TOPS · Houdini TOPs](https://tokeru.com/cgwiki/HoudiniTops.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
