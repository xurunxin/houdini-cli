# Karma / ROP 渲染与镜头级验收

ID: `render` · 领域: LOP / ROP · Skill: `houdini-render`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
以实际输出图和时间段为交付对象，区分技术通过与美术通过。

## 输入契约
相机、frame range、分辨率、renderer/device、输出路径、AOV、色彩、时长/内存预算。

## 推荐操作
1. 读取已有stage/ROP和输出设置，确认写入目录、依赖链及是否会覆盖文件。先单帧低采样，不直接全帧高质量渲染。
2. 核对当前XPU支持与设备状态，不把GPU内存简单相加；着色器编译与真正卡死要分辨。
3. 检查构图、光照、材质、体积、motion blur与景深，再提高采样。降噪可能改变细节，不把无噪点当唯一指标。
4. 技术验收看帧完整性、可解码、分辨率、AOV、NaN/Inf/黑帧；美术验收看轮廓、层次、主体可读性、风格与参考。
5. 动画验收需要连续回放并检查镜头/效果事件附近密集帧，不能用首中尾三张静帧代替全部时间行为。

## 验收条件
- 输出文件存在、可解码、帧号/尺寸/AOV符合约定。
- 视觉评估记录具体图像或时间段、问题和改动依据。
- 未做审美/动画复核时明确标记未验收。

## 症状 → 优先检查
**返回成功但无图**：查ROP输出、帧范围、依赖错误、内嵌业务结果与实际路径。
**黑帧**：检查相机、visibility、灯光、材质和曝光，不只提高采样。
**超时后重复渲染**：停止重放，先查询任务/文件状态；已有文件也可能来自旧版本。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Karma Render Settings`、`USD Render ROP`、`Camera`、`Dome Light`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html) — selected-sections；
- [S-SOLARIS · Solaris / USD](https://www.sidefx.com/docs/houdini/solaris/index.html) — index；
- [R-CLI · houdini-cli command implementation](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs) — file；
- [R-VALID · houdini-cli acceptance](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/docs/validation.md) — file；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
