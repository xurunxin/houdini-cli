# 示例与安全前提

所有示例为本包原创，不含下载来的第三方 HIP。HOM：离线语法与部分保护逻辑已检查；VEX：人工语义复核，未在Houdini编译。状态记录见 [examples索引](../index/examples.json)。

## HOM：通过现场 schema 封装

| 文件 | 行为 | 前置条件 |
| --- | --- | --- |
| [runtime_probe.py](hom/runtime_probe.py) | 版本/许可证类别/场景/FPS概要，无显式cook | 可连接的HOM；hython未保存标志不可靠 |
| [discover_node_types.py](hom/discover_node_types.py) | 按关键词/category列已安装类型 | 必须有筛选，不创建节点，不自动选择版本 |
| [inspect_node.py](hom/inspect_node.py) | 参数模板、连线、上次错误 | 显式node path；默认不求值，可分页 |
| [geometry_report.py](hom/geometry_report.py) | SOP输出计数、属性与点样本 | allow_cook=true；样本为前N点，不是全量验证 |
| [usd_report.py](hom/usd_report.py) | LOP stage少量prim与直接材质关系 | allow_cook=true；不解析全部binding强度或inactive prim |
| [build_sop_smoke.py](hom/build_sop_smoke.py) | 独立任务几何网络及包围盒检查 | allow_write=true、allow_cook=true；名称冲突停止 |

通过 `make_tool_args.py` 将本地脚本与配置嵌入已核对的代码字段。不要直接以系统Python执行需要HOM的脚本；`import hou`需要目标Houdini环境。脚本也可在经过许可的Houdini Python Shell中以相同config wrapper运行，但不要启动第二个MCP争抢当前桥接。

示例默认不授权真实修改/cook。`config/*.json`的path是示例路径，先改为现场目标。`build_sop_smoke`发生异常可能留下部分任务网络，不自动删除，必须检查；这比盲目重试或清空用户场景更安全。

## VEX：写明执行域和输入

[stable_scale](vex/stable_scale.vfl)：稳定point id驱动pscale，缺id明确标记。
[orient_from_normal](vex/orient_from_normal.vfl)：+Z原型对齐N；不承诺路径roll连续。
[rest_displacement](vex/rest_displacement.vfl)：从rest求形变，避免意外累积。
[sample_surface_color](vex/sample_surface_color.vfl)：第二输入曲面Cd插值，区分primitive UV与贴图UV。
[curl_velocity](vex/curl_velocity.vfl)：只产生v属性，不自动积分运动。
[growth_accumulation](vex/growth_accumulation.vfl)：明确Solver previous-state输入和增长属性。

代码顶部的Run Over、输入和属性前提是契约。写入已有Wrangle前先读取并保存旧代码；检查现场是否有专用 `create_wrangle` / `set_wrangle_code`，使用后检查validation。新的示例应单独命名，缺失属性标志非零时不能验收通过。

## 边界

这些脚本不是事务或安全沙箱。Houdini自身的回调、表达式、HDA和cook可能产生更广泛的副作用。只在可信、已审查的场景和明确修改范围内使用；不自动加载社区HIP或执行远程脚本。目标路径中仅有几个点也不能保证上游cook便宜。
