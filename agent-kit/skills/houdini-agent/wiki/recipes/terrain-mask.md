# 用坡度/地貌遮罩控制植被

ID: `recipe-terrain-mask` · Skill: `houdini-terrain` · **recipe-design-not-runtime-tested**

## 输入
覆盖范围/米制尺度、分辨率、种子、坡度、侵蚀时间、输入DEM数据及坐标参考。

## 最小网络意图
`HeightField → Erode/masks → Scatter → Packed prototypes`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
单位、mask层、坡度范围、密度、原型尺度

## 执行
1. 先验证地形高度和水平尺度，再确认mask层的数值范围。
2. 少量散布检查陡坡、谷地和边缘位置。
3. 拓展密度后检查原型朝向与实例内存。

## 验收
- mask与地貌对应，植被没有无意覆盖禁区。
- 原型尺寸与地形比例一致，输出层可追溯。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../16-terrain.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-TERRAIN · Heightfields SOP](https://www.sidefx.com/docs/houdini/heightfields/index.html)
- [S-TERRAINCOP · Copernicus heightfields](https://www.sidefx.com/docs/houdini/heightfields_cop/index.html)
- [E-TERRAIN · Entagma: Heightfields on 3D Objects / Houdini 22](https://entagma.com/heightfields-on-3d-objects-modding-houdini-22/)
