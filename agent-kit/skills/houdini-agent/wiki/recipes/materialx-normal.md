# MaterialX 法线贴图与颜色语义验证

ID: `recipe-materialx-normal` · Skill: `houdini-render` · **recipe-design-not-runtime-tested**

## 输入
目标delegate、材质路径、贴图和UDIM、UV/primvars、图像语义与OCIO/view transform。

## 最小网络意图
`UV/primvar → Texture/vector data → Normal mapping → Material output`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
纹理语义、UV名字、tangent convention、data colorspace

## 执行
1. 确认读取UV和正确通道；normal应作为向量数据处理。
2. 在中性灯光下对比贴图开/关，查看轴向是否反转。
3. 检查接缝和粗糙度等其他因素是否掩盖normal问题。

## 验收
- 没有错误颜色转换。
- 凹凸方向和接缝符合目标材质。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../22-materials.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-MTLX · MaterialX in Solaris](https://www.sidefx.com/docs/houdini/solaris/materialx.html)
- [S-XPU · Karma XPU](https://www.sidefx.com/docs/houdini/solaris/karma_xpu.html)
- [C-LOPS · Houdini LOPs](https://tokeru.com/cgwiki/HoudiniLops.html)
