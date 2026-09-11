"""Process-scoped Houdini CLI bootstrap. Loaded only through the launch environment."""

import importlib.util
import os
import sys


def _load_houdini_mcp(source):
    existing = sys.modules.get("houdinimcp")
    if existing is not None:
        return existing
    init_path = os.path.join(source, "__init__.py")
    spec = importlib.util.spec_from_file_location(
        "houdinimcp", init_path, submodule_search_locations=[source]
    )
    if spec is None or spec.loader is None:
        raise ImportError("Unable to load Houdini MCP from %s" % source)
    module = importlib.util.module_from_spec(spec)
    sys.modules["houdinimcp"] = module
    spec.loader.exec_module(module)
    return module


if os.environ.get("HOUDINI_CLI_AUTOSTART") == "1":
    _source = os.environ["HOUDINI_CLI_MCP_SOURCE"]
    _host = os.environ.get("HOUDINI_CLI_MCP_HOST", "127.0.0.1")
    _port = int(os.environ.get("HOUDINI_CLI_MCP_PORT", "9877"))
    _load_houdini_mcp(_source).start_server(host=_host, port=_port)
