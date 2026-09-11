# 在全序列前执行可比的单帧预览

ID: `recipe-render-one-frame` · Skill: `houdini-render` · **recipe-design-not-runtime-tested**

## 输入
相机、frame range、分辨率、renderer/device、输出路径、AOV、色彩、时长/内存预算。

## 最小网络意图
`Validated stage/ROP → Low-cost single frame → Image review`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
相机、输出路径、帧、分辨率、采样、AOV、色彩

## 执行
1. 读取现有ROP/renderer与输出依赖，确认写目录和覆盖权限。
2. 低分辨率单帧渲染；记录所有参数和时间。
3. 检查画面内容和技术输出后才扩大帧段。

## 验收
- 真实图像可打开，视图和目标一致。
- 未通过项有明确原因，不因工具成功直接渲染整片。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../23-render.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html)
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html)
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs)
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md)
