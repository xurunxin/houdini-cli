# 选择 SOP 或 Copernicus 地形路径

ID: `recipe-terrain-cop-route` · Skill: `houdini-terrain` · **recipe-design-not-runtime-tested**

## 输入
覆盖范围/米制尺度、分辨率、种子、坡度、侵蚀时间、输入DEM数据及坐标参考。

## 最小网络意图
`Version probe → Workflow choice → Minimal terrain → Conversion/output`

**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。

## 必须现场查询的参数/契约
安装版本、图像/体积域、层、导入导出

## 执行
1. 根据当前安装确认两种工作流是否存在。
2. 需要在3D对象表面组织地形时继续查H22专题及对应节点，不从landing页猜参数。
3. 先验证转换出口和单位，再迁移旧网络中的mask/erosion思路。

## 验收
- 所选路径的输入/输出表示明确。
- 未混用新旧节点参数，并保留转换测试证据。

风险: `scene-write-or-cook`。只在已授权路径与任务命名空间执行；不重放超时未知操作。

进一步阅读：[领域卡](../16-terrain.md) · [执行协议](../02-cli-contract.md)

## 来源
- [S-TERRAIN · Heightfields SOP](https://www.sidefx.com/docs/houdini/heightfields/index.html)
- [S-TERRAINCOP · Copernicus heightfields](https://www.sidefx.com/docs/houdini/heightfields_cop/index.html)
- [E-TERRAIN · Entagma: Heightfields on 3D Objects / Houdini 22](https://entagma.com/heightfields-on-3d-objects-modding-houdini-22/)
