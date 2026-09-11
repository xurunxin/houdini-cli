# Copernicus 程序贴图的导出验收

ID: `recipe-texture-output` · Skill: `houdini-copernicus` · **recipe-design-not-runtime-tested**

## 输入
图像/几何输入、层/通道、分辨率、像素/世界空间、颜色与数据语义、目标输出格式。

## 最小网络意图
`Low-res graph → Channel/range check → Final resolution → Image output`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
分辨率、位深、通道、alpha、颜色/数据图

## 执行
1. 先检查层、通道和数值范围，再提高分辨率。
2. 记录normal/height/mask与颜色图的不同解释。
3. 在目标材质中读回，检查tile、边缘与alpha。

## 验收
- 格式/通道/位深符合接收端。
- 实际材质使用结果与设计一致。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../24-copernicus.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-COP · Copernicus](https://www.sidefx.com/docs/houdini/copernicus/index.html)
- [C-COPS · Legacy Houdini COPs](https://tokeru.com/cgwiki/HoudiniCops.html)
- [S-TERRAINCOP · Copernicus heightfields](https://www.sidefx.com/docs/houdini/heightfields_cop/index.html)
