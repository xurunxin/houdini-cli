# 缓存、导入导出、路径与交付

ID: `cache-io` · 领域: SOP / ROP / USD · Skill: `houdini-pdg`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
形成可读回、可定位来源、不会误覆盖的交付包。

## 输入契约
保存范围、格式/许可证限制、相对路径基准、可用空间、外部资产、颜色/单位/FPS。

## 推荐操作
1. 选择数据保真需要的格式：Houdini几何缓存、体积、动画几何、骨骼、USD场景分开；不能假设单一格式保留所有属性。
2. 文件名包含资产/版本/帧；保持$HIP/$JOB与实际展开路径一致。对保存场景解释会改变当前hip身份和相对路径基准。
3. 写前检查目标目录和覆盖权限；不同资产/变体不得共享可写文件名。不要通过改扩展名绕过.hiplc/.hipnc及格式授权限制。
4. 完成后查帧范围、大小、解码/读回以及关键属性；另存或加载只在明确用户意图下执行，不自动清空当前场景。

## 验收条件
- 文件清单与帧范围完整，格式读回正确。
- 单位/轴/FPS与必要属性在接收端保留。
- 依赖路径和来源版本可追溯；没有未经许可覆盖。

## 症状 → 优先检查
**重开场景缓存找不到**：核对$HIP/$JOB变化、相对路径和交付目录。
**只输出一帧**：查frame token与范围模式。
**输出存在但过期**：比较输入/版本清单而非仅mtime。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`File Cache`、`File`、`Alembic`、`FBX`、`USD ROP`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-CACHE · File Cache SOP](https://www.sidefx.com/docs/houdini/nodes/sop/filecache.html) — selected-sections；
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html) — index；
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html) — index；
- [R-README · houdini-cli README](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/README.md) — file；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
