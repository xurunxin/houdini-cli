# 渲染动画闪烁的分层定位

ID: `recipe-render-flicker` · Skill: `houdini-render` · **recipe-design-not-runtime-tested**

## 输入
相机、frame range、分辨率、renderer/device、输出路径、AOV、色彩、时长/内存预算。

## 最小网络意图
`Cached scene → Short raw render sequence → Compare denoised → Review`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
时间采样、稳定属性、灯光/纹理、采样、降噪

## 执行
1. 先排除几何/粒子/属性的时间不稳定。
2. 固定缓存和灯光，比较未降噪与降噪序列。
3. 在问题帧段逐帧与连续回放结合定位，不一次调全部参数。

## 验收
- 问题归因于场景、采样或后处理的证据明确。
- 修复前后同条件序列可比较。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../23-render.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html)
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs)
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md)
