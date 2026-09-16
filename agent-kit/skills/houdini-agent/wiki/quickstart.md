# 快速上手：从离线检索到一次可核对的调用

本页是首次接入的示例，不是每项任务的固定流程。已知领域或知识卡时直接使用；复用已核对的会话、schema 和现有网络，只执行当前任务需要的部分。

## 1. 先查询，不启动 Houdini

以下在解压后的项目根目录执行；安装后的路径改用 `.agents/skills/houdini-agent`。`python` 需为 Python 3.10+。

```powershell
python skills/houdini-agent/tools/query.py search "烟不显示" --limit 3
```

打开命中页面，确认输入与验收。只需要知识问答时，到这里即可；不要为读文档启动应用。

## 2. 建立或复用当前目标的任务会话

以下适用于已经能正常使用的 `houdini-cli`。没有环境时先 `doctor`，只在缺失/损坏时查看 `setup --help` 并初始化，不每次重装。

```powershell
houdini-cli session status
# 确认不存在其他目标占用；task名仅示例，可用自己的任务名。
houdini-cli session start wiki-smoke --launch-app
houdini-cli --session wiki-smoke tools list
```

不要为抢占连接结束别人的任务；同桥接的工具调用串行进行。已有应用没有桥接时，保留场景并协调接入，不擅自重启。

## 3. 优先使用只读专用工具

只有上一步列表中存在对应名称时，才执行：

```powershell
houdini-cli --session wiki-smoke tools inspect get_scene_info
# 检查实际schema；固定上游的此工具不需业务参数。
houdini-cli --session wiki-smoke tools call get_scene_info --args '{}'
```

其他工具逐个inspect。`get_parameter_schema`会取当前值/菜单等信息，可能比纯元数据读取成本高；限定path、pattern与分页。它不是保证无任何表达式求值的操作。

## 4. 仅在专用工具不足时封装 HOM

`execute_houdini_code` 和 `code` 在固定上游已见，但你的定制服务可能不同；**必须检查实时schema**。代码文件不直接传给Houdini做文件读取，而由打包工具嵌入为字符串。

```powershell
$task = "wiki-smoke"
$tool = "execute_houdini_code" # 仅在 tools list 中确实存在时使用。
$json = & houdini-cli --session $task tools inspect $tool
if ($LASTEXITCODE -ne 0) { throw "tools inspect failed" }
# Windows PowerShell 5.1 的 > 默认编码不同，显式用 UTF-8 无 BOM 保存。
[IO.File]::WriteAllText(
  (Join-Path $PWD "execute-schema.json"),
  ($json -join "`n"),
  [Text.UTF8Encoding]::new($false)
)

# 打开 execute-schema.json，确认 code 为真实输入字段后再运行。
python skills/houdini-agent/tools/make_tool_args.py `
  --schema execute-schema.json `
  --code-field code `
  --script skills/houdini-agent/examples/hom/runtime_probe.py `
  --config skills/houdini-agent/examples/config/runtime-probe.json `
  --output runtime-probe-args.json
if ($LASTEXITCODE -ne 0) { throw "argument packaging failed" }

# 审查生成参数文件；这一步才真正调用现场Houdini。
$result = & houdini-cli --session $task tools call $tool --args-file runtime-probe-args.json
$callExit = $LASTEXITCODE
[IO.File]::WriteAllText(
  (Join-Path $PWD "runtime-probe-result.json"),
  ($result -join "`n"),
  [Text.UTF8Encoding]::new($false)
)
python skills/houdini-agent/tools/inspect_result.py runtime-probe-result.json
# 同时审查 $callExit 和上一步状态；unknown 不是 pass。
```

打包器默认拒绝覆盖现有 args 文件，避免误修改正在执行或需要追溯的请求。要再发新请求，另取文件名；不要覆盖后直接重发。

## 5. 做小网络 smoke（可选，属于真实写操作）

仅需要验证基础建网能力时执行本例，不把它作为每次编辑或渲染的前置步骤。先读取 [示例前提](../examples/README.md)。复制 `build-sop-smoke.json` 到任务工作目录，明确设置允许修改与cook后，才将两个allow字段设true，再按上节打包/调用 `build_sop_smoke.py`。

它仅创建 `/obj/AGENT_smoke01` 内的 Box → Transform → OUT，并检查包围盒；不删除/清空/保存/渲染。若名称已存在就停止。超时后先查该路径，不换个名字盲目重跑。验收该例只说明基本网络操作有效，不代表Vellum/Pyro/Karma已通过。

## 6. 检查产物与释放 MCP

```powershell
python skills/houdini-agent/tools/validate_sequence.py `
  --root "D:/renders/test" --pattern "shot.{frame:04d}.exr" --start 1 --end 24

# 默认只释放任务MCP，保留应用和现场。
houdini-cli session status wiki-smoke
houdini-cli session end wiki-smoke
```

序列工具只检查文件结构。还需解码、目标节点/字段检查、动画回放与视觉复核；现有同名文件可能来自旧版本。

## 返回码

CLI：0成功、1运行/工具错误、2参数错误。`inspect_result.py`：0仅“报告了业务成功”、1失败、2输入错误、3未知。`check_acceptance.py`：0仅“清单报告通过”、1有失败、2清单无效、3仍有未验证项。代码0都不自动等于艺术交付通过。

来源：[CLI实现](https://github.com/xurunxin/houdini-cli/blob/57a8e81de4a8f372f6dda4de6ab2fffee11e4bb9/src/cli.mjs)、[上游工具实现](https://github.com/capoomgit/houdini-mcp/blob/de4fd93acc207fc57c02b330d421461f5963a945/houdini_mcp_server.py)。
