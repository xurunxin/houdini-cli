# 检查缓存序列完整性并读回

ID: `recipe-cache-readback` · Skill: `houdini-pdg` · **recipe-design-not-runtime-tested**

## 输入
保存范围、格式/许可证限制、相对路径基准、可用空间、外部资产、颜色/单位/FPS。

## 最小网络意图
`Expected manifest → File-structure check → Controlled readback → Attributes review`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
帧范围、frame token、版本、必需属性、空间

## 执行
1. 使用validate_sequence仅检查存在性与非零大小。
2. 通过另一受控读取路径解码并检查关键属性/字段。
3. 比较输入版本和缓存清单，排除旧文件误命中。

## 验收
- 所有预期帧已检查，缺帧明确报告。
- 数据解码/语义和版本一致；结构检查不冒充内容检查。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../27-cache-io.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-CACHE · File Cache SOP](https://www.sidefx.com/docs/houdini/nodes/sop/filecache.html)
- [S-INDEX · Houdini 文档总入口](https://www.sidefx.com/docs/houdini/index.html)
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [R-README · houdini-cli README](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/README.md)
