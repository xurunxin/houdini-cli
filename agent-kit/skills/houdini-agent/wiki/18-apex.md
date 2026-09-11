# APEX：角色图与动画系统入口

ID: `apex` · 领域: APEX / SOP · Skill: `houdini-character`
覆盖等级: **discovery** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
将APEX图构建、角色场景和最终变形分离。

## 输入契约
当前APEX节点/图API版本、骨架与几何、组件约定、命名和角色打包结构。

## 推荐操作
1. 先读取当前版本角色/APEX示例及现场节点；APEX图不是普通SOP节点图，不能逐节点直接套用所有HOM网络操作。
2. 用最小角色构建可检查的输入/输出契约，再加入组件、控制器和动画。记录自定义组件来源与版本。
3. 先测试静态pose和单关节控制，再测试约束、多角色和动画采样。
4. 遇到组件签名变化时停在适配层，保留已生成内容；不要把旧CGWiki节点名当作API兼容承诺。

## 验收条件
- 角色可加载、控制与变形链连通。
- 命名无冲突，关键pose回放可复现。
- 版本与组件来源可追溯。

## 症状 → 优先检查
**APEX图有数据但角色不动**：检查图I/O绑定与角色打包属性。
**旧教程不适用**：定位目标版本官方教程并重新发现组件/接口。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`APEX Scene Add Character`、`APEX Scene Animate`、`APEX Autorig Component`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-CHAR · Character / KineFX / APEX](https://www.sidefx.com/docs/houdini/character/index.html) — index；
- [C-APEX · Houdini APEX](https://tokeru.com/cgwiki/HoudiniApex.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
