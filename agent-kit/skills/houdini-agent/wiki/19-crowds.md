# Crowds：Agent、状态与动作混合

ID: `crowds` · 领域: SOP / DOP · Skill: `houdini-character`
覆盖等级: **discovery** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
规划人群工作流的入口、依赖与验收，不冒充完整群集系统实现。

## 输入契约
角色agent定义、动作clips、状态机、导航/障碍、人数、接触与变形需求。

## 推荐操作
1. 先用一个agent验证骨架、clip与单位，再少量agent测试动作状态切换。
2. 状态/触发条件与速度、根运动匹配；导航和障碍碰撞先于人数扩张。
3. 规划packed agent、变形和渲染预算；记录clip授权与依赖，最后再扩展数量。

## 验收条件
- clip范围和循环衔接正确。
- 状态切换无明显跳姿，路径和障碍符合预期。
- 输出支持目标渲染/导出路径。

## 症状 → 优先检查
**滑步/跳步**：检查clip根运动与模拟速度的对应。
**扩大人数后失败**：检查变形、代理与渲染资源，不仅降低模拟子步。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Agent`、`Agent Clip`、`Crowd Source`、`Crowd Solver`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-CROWDS · Crowds](https://www.sidefx.com/docs/houdini/crowds/index.html) — index；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
