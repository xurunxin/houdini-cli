"""Keep a Houdini Python process and its Qt-driven MCP socket bridge alive."""

import os
import runpy
import sys

from PySide6 import QtCore


if os.environ.get("HOUDINI_CLI_AUTOSTART") != "1":
    raise RuntimeError("This runner may only be started by houdini-cli")

# The Qt application must exist before HoudiniMCPServer creates and starts its
# QTimer. Hython does not create a GUI application for us.
application = QtCore.QCoreApplication.instance() or QtCore.QCoreApplication([])

# Hython may have run the ready hook before executing this file, which creates
# a QTimer before a Qt application exists. Recreate that owned server after the
# application is available so the timer receives events.
existing_module = sys.modules.get("houdinimcp")
if existing_module is not None and existing_module.is_server_running():
    existing_module.stop_server()

# Hython normally loads ready.py from HOUDINI_PATH. Run the owned hook once more
# explicitly so headless behavior does not depend on a particular Houdini build's
# startup ordering. start_server() is idempotent if ready.py already ran.
version = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
ready = os.path.join(os.path.dirname(__file__), "python%slibs" % version, "ready.py")
runpy.run_path(ready, run_name="houdini_cli_headless_ready")

# The Qt event loop services HoudiniMCPServer's QTimer in hython.
raise SystemExit(application.exec())
