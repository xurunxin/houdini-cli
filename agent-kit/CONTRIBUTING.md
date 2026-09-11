# 维护与扩展

## 一条知识的进入流程

用户实际任务 → 检索现有topic/recipe → 匹配版本官方API/节点页 → 作者原始社区实践 → 输入/输出契约 → 最小实验 → 验收证据 → 入库。

官方负责能力和API定义，社区负责经验和更好的问题分解。二者冲突时检查版本、上下文和数据前提，不能单纯以网页发布时间替代适用性判断。

## 数据与生成视图

结构化条目位于 `skills/houdini-agent/index/topics.json` / `recipes.json`，用稳定id和实际路径关联。修改此处后运行：

```bash
python tools/rebuild_wiki.py
python tools/build_site.py
python tools/validate_kit.py .
python -m unittest discover -s tests -v
```

Wiki为可阅读视图，验证器会检查步骤与验收项是否与索引一致。手工编辑的quickstart、tool-map、target-smoke等操作文档不由topic重建器覆盖。领域Skill应保持短，只保留路由/动作/门槛；领域契约发生变化时同步审查对应Skill。

## 来源登记

为每个来源设置id、url、kind、reviewed_on、review_depth和pin_kind。允许`index`、`landing-only`、`article`、`selected-sections`、`file`等深度。未完整观看视频或运行HIP就不要写成完整复现。网页hash未知为null；只有确实下载并计算后才填写。访问失败的页面不登记为已审阅，可另记为待查线索。

Git来源固定到实际commit。更新CLI需对比命令、JSON封装、session冲突、超时和installer行为。工具候选不是JSON Schema仓库；现场schema每次环境改变后重新发现。

## 新配方要求

写明输入、minimum_network（概念而非保证存在的内部名）、parameters_to_discover、steps、acceptance、风险、覆盖等级、来源及示例路径。避免无前提的万能参数值，给出现场调参顺序与观察指标。新增领域应同时加入检索别名、中英文查询测试、专业skill路由和最小现场测试设计。

## 证据与等级

`guide` / `discovery`记录文档深度，不宣称运行通过。配方设计默认`recipe-design-not-runtime-tested`。当前例子统一`runtime_tested:false`。未来准备升级验证状态时，先引入独立运行证据清单并调整验证器策略，不直接删掉诚实边界。

## 权限和版权

社区示例文件可能含HDA、事件脚本和环境依赖，不能自动信任执行；先审查、隔离并征得所需授权。只收原创摘要、原理和链接；不把付费视频、第三方HIP或整站文档塞进仓库。新增依赖记录许可证，不在源码或日志中写凭据。
