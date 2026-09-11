"""HOM runtime metadata. Does not change frame, cook explicitly, save, or close.
Sources: S-HOM, S-HIP, S-LICENSE, S-NODE. Static-checked; not run in Houdini here.
"""
from __future__ import annotations
import sys

def run(config: dict) -> dict:
    import hou
    limit = config.get("limit", 30)
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 200:
        raise ValueError("limit must be 1..200")
    ui = hou.isUIAvailable()
    obj = hou.node("/obj")
    nodes = obj.children() if obj is not None else ()
    return {"ok": True, "application_version": hou.applicationVersionString(),
            "python_version": sys.version.split()[0], "ui_available": ui,
            "license_category": str(hou.licenseCategory()), "fps": hou.fps(), "frame": hou.frame(),
            "hip_path": hou.hipFile.path(),
            "has_unsaved_changes": hou.hipFile.hasUnsavedChanges(),
            "unsaved_flag_reliable": ui,
            "unsaved_note": "hython always reports True; this is not a safe-close authorization",
            "obj_children": [{"path": n.path(), "type": n.type().nameWithCategory()} for n in nodes[:limit]],
            "children_total": len(nodes), "truncated": len(nodes) > limit,
            "explicit_cook_requested": False}

if __name__ == "__main__":
    import json
    try:
        _result = run(globals().get("HOUDINI_AGENT_CONFIG", {}))
        _encoded = json.dumps(_result, ensure_ascii=False, allow_nan=False, default=str)
    except Exception as _error:
        _result = {"ok": False, "error_type": type(_error).__name__, "error": str(_error),
                   "note": "Inspect current scene state before any retry; no automatic rollback."}
        _encoded = json.dumps(_result, ensure_ascii=False, allow_nan=False)
    print("HOUDINI_AGENT_RESULT=" + _encoded)
