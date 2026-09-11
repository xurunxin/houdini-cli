# Pyro：源、字段、模拟与烟火外观

ID: `pyro` · 领域: SOP / DOP / LOP · Skill: `houdini-pyro`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
把“有没有烟数据”“动得对不对”“渲染好不好看”分三层诊断。

## 输入契约
源几何与持续时间、字段名/类型、体素尺寸、域/边界、碰撞、散热和外观需求。

## 推荐操作
1. 先证明源字段存在且位置正确；按当前solver要求匹配density、temperature、vel等，不凭材质参数弥补缺数据。
2. 低分辨率跑短帧段确认注入、上升/扩散、碰撞和域范围。Sparse不代表任意扩大域都无内存成本。
3. 大尺度运动确定后再加disturbance、shredding等细节；不要同时改变分辨率和所有扰动参数。
4. 缓存必要字段并检查读回；模拟字段与渲染/着色字段转换分开。体积在viewport可见不保证Karma材质连接正确。

## 验收条件
- 源、solver、cache三个位置都能证实字段和active bounds。
- 连续运动无异常重置、边界裁切或明显时间闪烁。
- 低分辨率渲染检查密度、发光、曝光和颜色空间。

## 症状 → 优先检查
**烟不显示**：逐段查source→rasterize→solver→cache→shader；字段存在后才调显示范围。
**爆炸被方盒切断**：查active区域、边界与source扩展。
**缓存巨大**：先核对字段、域和分辨率，不盲目删除渲染/重定时需要的字段。

## 版本与边界
CGWiki含旧DOP/旧Pyro内容。现代SOP Pyro与旧shelf网络要分开标记；参数和接线不能直接混用。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Pyro Source`、`Volume Rasterize Attributes`、`Pyro Solver`、`Pyro Bake Volume`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-PYRO · Pyro](https://www.sidefx.com/docs/houdini/pyro/index.html) — index；
- [S-PYROSOLVER · Pyro Solver SOP](https://www.sidefx.com/docs/houdini/nodes/sop/pyrosolver.html) — selected-sections；
- [S-PYROLOOK · Pyro workflow/lookdev](https://www.sidefx.com/docs/houdini/pyro/lookdev.html) — article；
- [C-PYRO · Smoke and Pyro (mixed/legacy)](https://tokeru.com/cgwiki/Smoke_and_Pyro.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
