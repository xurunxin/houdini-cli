# MaterialX、纹理、颜色空间与Lookdev

ID: `materials` · 领域: LOP / VOP · Skill: `houdini-render`
覆盖等级: **guide** · 来源复核: 2026-09-11 · **目标 Houdini 运行验收：未执行**

## 适用目标
建立与渲染器兼容的材质，并在可比较的光照下验收。

## 输入契约
目标delegate、材质路径、贴图和UDIM、UV/primvars、图像语义与OCIO/view transform。

## 推荐操作
1. Karma材质优先在匹配的Material Builder中建立，严格MaterialX互操作需求单独标记；传统VEX材质不是XPU通用兼容路径。
2. 先用中性灯光与简单表面检查base color、roughness和normal；颜色图与数值数据图分开解释，不对法线向量做颜色转换。
3. 检查UV/geomprop读取的名字、类型和插值；贴图存在并不代表shader读取了正确坐标。
4. 记录纹理路径与视图变换，在同曝光/灯光/相机下比较修改，不用同时改环境掩盖材质问题。

## 验收条件
- 材质节点合法、绑定正确、纹理可解析。
- 数据图没有错误gamma/颜色变换。
- 目标渲染器的测试图和AOV符合任务需求。

## 症状 → 优先检查
**法线方向怪**：确认贴图为向量数据、tangent convention与normal处理链。
**XPU和CPU外观不同**：查当前功能支持与shader路径，不宣称两引擎全功能等价。

## 版本与边界
节点全名、参数和输入输出以目标 Houdini 实时查询及匹配版本 Help 为准。

节点/工具候选（检索词，不是保证可调用的内部类型名）：`Material Library`、`Karma Material Builder`、`USD MaterialX Builder`、`MtlX Standard Surface`

统一执行协议见 [CLI 契约](02-cli-contract.md)；验收分层见 [验收卡](31-acceptance.md)。

## 来源与进一步查询
- [S-MTLX · MaterialX in Solaris](https://www.sidefx.com/docs/houdini/solaris/materialx.html) — article；
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html) — selected-sections；
- [C-LOPS · Houdini LOPs](https://tokeru.com/cgwiki/HoudiniLops.html) — selected-sections；

以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。
