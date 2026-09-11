"""Discover installed node types without instantiating them. Sources: S-NODETYPE, S-HOM."""
from __future__ import annotations

def run(config: dict) -> dict:
    import hou
    query = str(config.get("query", "")).strip().casefold()
    category = str(config.get("category", "")).strip().casefold()
    limit = config.get("limit", 40)
    if not query and not category:
        raise ValueError("provide query or category; refuse an unbounded type dump")
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1 <= limit <= 200:
        raise ValueError("limit must be 1..200")
    rows=[]; total=0
    for cat in hou.nodeTypeCategories().values():
        if category and cat.name().casefold() != category:
            continue
        for nt in sorted(cat.nodeTypes().values(), key=lambda n: n.name()):
            if query and query not in (nt.name()+" "+nt.description()).casefold():
                continue
            total += 1
            if len(rows) >= limit:
                continue
            rows.append({"category":cat.name(), "name":nt.name(), "qualified_name":nt.nameWithCategory(),
                         "label":nt.description(), "name_components":list(nt.nameComponents()),
                         "min_inputs":nt.minNumInputs(), "max_inputs":nt.maxNumInputs(),
                         "max_outputs":nt.maxNumOutputs(), "help_url":nt.helpUrl(),
                         "default_help_url":nt.defaultHelpUrl()})
    return {"ok": True,"query":query,"category":category,"matches":rows,"match_count":total,
            "truncated":total > len(rows), "created_nodes":False,
            "note":"nameComponents order = scope, namespace, core_name, version; no automatic version selection"}

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
