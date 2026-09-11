# Validation — 2026-09-11

## v0.2 task lifecycle

- A named task reused the existing Houdini GUI and single-client bridge without restarting the application.
- Separate `get_scene_info` and tool-schema CLI invocations shared one MCP process (PID 30240 during this acceptance).
- `session end` closed the task MCP and retained Houdini and its bridge.
- Shared tests cover task reuse, active-request protection, timeout without replay/reconnect, idle-only MCP cleanup, startup failure and ownership-safe native close. Headless application closure remains explicitly retained because there is no generic save-preserving native window close.

## v0.1 bootstrap baseline

Platform: Windows, Node.js 24.20.0, Houdini 22.0.368 (Python 3.13.10 / PySide6 6.8.3).

- Clean installation: an isolated alternate CLI home fetched pinned upstream commit `de4fd93acc207fc57c02b330d421461f5963a945`, installed pinned Python requirements, imported its generated MCP bridge, and launched a headless Houdini instance. A live `get_scene_info` call succeeded against `untitled.hip`. That test-owned application process was then stopped.
- The headless acceptance exposed an early Qt timer initialization issue. The headless runner now recreates the owned server after its QCoreApplication exists; the repeated real read-only call passed.
- Existing installation: the machine's default CLI home was configured with its current customized Houdini MCP source. Dependencies and generated files went to the CLI state directory; the original Git checkout remained dirty with the same five modified files and was preserved.
- `app launch` started graphical Houdini and waited for `127.0.0.1:9877`.
- `tools list` discovered 25 tools from the current customized source, including its node inspection/editing and render tools.
- `tools inspect get_scene_info` returned the current schema; `tools call get_scene_info` returned `untitled.hip`, 24 fps, frame range 1–240, and empty node contexts.
- The common MCP tests verify per-request stdio lifecycle, pagination, tool errors, timeout, startup failure, and child-process cleanup. Adapter tests cover isolated source handling, numeric application-version discovery, headless/bootstrap construction, loopback restrictions and asynchronous launch errors.

Acceptance performed read-only scene queries. Editing, rendering, OPUS/RapidAPI usage, other Houdini versions/license types, and macOS/Linux execution have not been accepted. The commercial application and licenses are not distributed or installed by this CLI.
