# Houdini setup

`houdini-cli` separates the application bridge from its MCP runtime:

1. Houdini runs a TCP bridge on `127.0.0.1:9877`.
2. `session start <task>` keeps one MCP stdio process for the target task. Commands using `--session <task>` reuse that connection until `session end` or idle cleanup. Without a task session, a one-shot command closes its own MCP process after the request.

The Houdini application remains open when the stdio process exits. The TCP bridge is intentionally loopback-only because the upstream tool set includes scene changes and arbitrary Houdini Python execution.

## Requirements

- Windows with SideFX Houdini. Setup discovers versioned installations under `Program Files\Side Effects Software` from newest to oldest, then checks `houdini.exe` on `PATH`. The tested installation is Houdini `22.0.368`.
- Git, used only when setup downloads the pinned upstream source.
- `uv` on `PATH`, or an explicit `--uv-path`.
- A valid Houdini license. Headless mode uses `hython` and may check out a Batch, Engine, or FX license.

The tested Houdini build embeds Python `3.13.10`, PySide6 `6.8.3`, and Qt `6.8.3`. `doctor` runs a bounded `hython` probe to verify Python and PySide6 for the configured installation.

## Clean setup

Preview the exact paths first:

```powershell
houdini-cli setup --dry-run
```

Then install:

```powershell
houdini-cli setup
```

With no `--source`, setup downloads `capoomgit/houdini-mcp` at commit `de4fd93acc207fc57c02b330d421461f5963a945`. It creates an isolated uv project under the CLI state directory and pins the v1 MCP SDK (`mcp[cli]==1.4.1`). The upstream bridge imports `mcp.server.fastmcp`, which was removed in MCP SDK v2.

Setup generates its own bridge copy in the state directory. If an older source uses the moved LangChain output-parser import, the generated copy is patched to prefer `langchain_classic.output_parsers`. The selected source checkout is never patched or synchronized by uv.

## Reuse an existing source checkout

This uses the current local checkout without changing it:

```powershell
houdini-cli setup `
  --source 'D:\Tools\houdini-mcp' `
  --app-path 'C:\Program Files\Side Effects Software\Houdini 22.0.368\bin\houdini.exe'
```

The source directory must contain `__init__.py`, `server.py`, `HoudiniMCPRender.py`, and `houdini_mcp_server.py`. A custom stdio entry point can be selected with `--server-path`; dependencies still install into the CLI-owned runtime.

`doctor` reports an external Git checkout's revision and dirty state. A dirty checkout is supported and remains untouched.

## Start and verify

Run the read-only checks:

```powershell
houdini-cli doctor
```

Launch the graphical application and wait until its loopback bridge is ready:

```powershell
houdini-cli app launch
```

The launch environment temporarily prepends a CLI-owned Houdini path. Houdini's standard path remains present through `&`, so packages, user preferences, and factory content continue to load. The CLI does not write `houdini.env`, the user package directory, shelves, scenes, or preferences. The startup hook is active only for a process launched by this command.

For a non-graphical session:

```powershell
houdini-cli app launch --headless
```

Logs are written under the CLI state directory in `logs`. The launch command waits for `127.0.0.1:9877` and reports a timeout or early process exit with the log path.

Discover the live tool schemas:

```powershell
houdini-cli tools list
houdini-cli tools inspect get_scene_info
```

`get_scene_info` is the safe read-only smoke test. It reads the current scene name, frame range, and top-level node summaries:

```powershell
houdini-cli tools call get_scene_info --args '{}'
```

Run one CLI tool request at a time. The upstream Houdini bridge has one active client slot and replaces an older client when a new MCP stdio process connects.

## Operational boundaries

- `get_scene_info`, `get_parameter_schema`, `find_error_nodes`, `get_geometry_info`, and `get_geometry_data` are inspection tools. Some may cook or traverse scene data; inspect the live schema before use.
- Creation, deletion, parameter, wiring, layout, wrangle, import, and render tools can change the scene or produce files.
- `execute_houdini_code` executes arbitrary Python inside Houdini and should be reserved for operations without a dedicated tool.
- OPUS tools require separate RapidAPI settings in `urls.env`; setup does not create credentials.
- The bridge is not an authentication boundary. Keep it on loopback and do not proxy port `9877` to another host.
- `houdini-cli` launches a new Houdini process. It does not inject the bridge into an already-running process.

Official references: [Houdini Path](https://www.sidefx.com/docs/houdini/basics/houdinipath.html), [Python startup script locations](https://www.sidefx.com/docs/houdini/hom/locations), [Hython and command-line scripting](https://www.sidefx.com/docs/houdini/hom/commandline), and the [MCP Python SDK v2 changes](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/whats-new.md).
