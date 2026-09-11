# 毛发、羽毛与肌肉工作流导航

ID: `groom` · 领域: SOP / DOP · Skill: `houdini-character`
覆盖等级: **discovery** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
为专用角色二级系统定位正确官方入口，并定义最小验证方案。

## 输入契约
皮肤rest/动画、稳定拓扑或转移方法、引导曲线、材质和模拟需求。

## 推荐操作
1. 毛发先测试guide生成、skin绑定及动画跟随，再扩展渲染毛数量。
2. 羽毛先分离设计、分布、变形与渲染表示；记录当前版本要求的属性/组。
3. 肌肉走专门组织/肌肉流程，先检查骨骼驱动和rest配置，不将任意软体求解器当成等价替代。
4. 本卡只负责检索与验收框架；具体网络必须继续读取对应版本的专题与节点Help。

## 验收条件
- 静止与极限姿态均检查跟随、穿插、厚度。
- 明确模拟/变形与渲染细节的预算界线。
- 记录实际阅读的专用节点页和运行证据。

## 症状 → 优先检查
**毛发浮离皮肤**：检查rest皮肤、UV/属性匹配和坐标空间。
**羽毛或肌肉效果异常**：先验证绑定及输入数据，而不是只改渲染器。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Guide Groom`、`Hair Generate`、`Feather`、`Muscle`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-FUR · Hair and fur](https://www.sidefx.com/docs/houdini/fur/index.html) — index；
- [S-FEATHERS · Feathers](https://www.sidefx.com/docs/houdini/feathers/index.html) — index；
- [S-MUSCLE · Muscles](https://www.sidefx.com/docs/houdini/muscles/index.html) — index；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
