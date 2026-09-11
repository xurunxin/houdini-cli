# VEX / VOP：小数据契约到批量计算

ID: `vex` · 领域: SOP / VEX / VOP · Skill: `houdini-vex`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
用 VEX 处理并行几何计算，用 HOM 管网络，不把两个执行模型混在一起。

## 输入契约
Run Over、输入编号、每个输入的属性与坐标空间、必要的 spare parameters、是否有时间反馈。

## 推荐操作
1. 从点/面/细节/体积执行域出发确定代码。input 0 与 1 的约定明确到接线；显式声明未知属性类型。
2. 先用最小几何测试一条计算，再扩展。ch/chf/chv 等通道引用必须先创建并验证参数，不能留下隐式零值。
3. 纯形变基于 rest/reference 计算；需要累积变化才放 Solver。拓扑变化前后都重新检查稳定 id。
4. 跨输入采样区分最近点、最近曲面 xyzdist+primuv、体积采样；primitive UV 参数不是贴图 UV。
5. 有顺序依赖的算法不要假设 point wrangle 的线程执行顺序。必要时使用 Detail 模式、小状态结构或重新设计并行数据流。

## 验收条件
- 代码编译无错误；类型和绑定 owner 正确。
- 零长度向量、空输入、负/极端参数有处理策略。
- 对同输入同 seed 重算符合稳定性约定。

## 症状 → 优先检查
**代码不报错但没效果**：确认 Run Over、group、输入编号、缺属性和通道。
**某几帧 NaN**：检查除零、normalize零向量、非法根号和溢出。
**每次 cook 都继续形变**：在不需要累积的地方误用反馈或修改后的 P；改读 rest。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Attribute Wrangle`、`Attribute VOP`、`Volume Wrangle`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-VEX · VEX snippets](https://www.sidefx.com/docs/houdini/vex/snippets.html) — article；
- [C-VEX · Houdini VEX](https://tokeru.com/cgwiki/HoudiniVex1.html) — selected-sections；
- [C-CHEAT · VEX cheat sheet](https://tokeru.com/cgwiki/VexCheatSheet.html) — selected-sections；
- [C-JOY · Joy of VEX](https://tokeru.com/cgwiki/JoyOfVex.html) — index；
- [J-VEX · John Kunz VEX Wrangle Snippets](https://wiki.johnkunz.com/index.php?title=VEX_Wrangle_Snippets) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
