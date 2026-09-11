"""Inspect bounded parameter metadata and connections; no default parm eval/menu scripts.
Sources: S-OPNODE, S-NODE, S-PARM, S-CONNECTION. Existing errors may be stale until cook.
"""
from __future__ import annotations

def run(config: dict) -> dict:
    import hou
    path=config.get("path")
    if not isinstance(path,str) or not path.startswith("/"):
        raise ValueError("an absolute Houdini node path is required")
    node=hou.node(path)
    if node is None or not isinstance(node,hou.OpNode):
        raise ValueError("path must resolve to an operator node")
    limit=config.get("limit",80); offset=config.get("offset",0)
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1 <= limit <= 300:
        raise ValueError("limit must be 1..300")
    if not isinstance(offset,int) or isinstance(offset,bool) or offset<0:
        raise ValueError("offset must be a nonnegative integer")
    pattern=str(config.get("contains","")).casefold()
    parms=[p for p in node.parms() if not pattern or pattern in (p.name()+" "+p.parmTemplate().label()).casefold()]
    rows=[]
    for p in parms[offset:offset+limit]:
        template=p.parmTemplate()
        row={"name":p.name(),"path":p.path(),"label":template.label(),
             "template_type":str(template.type()),"tuple_size":template.numComponents()}
        if config.get("allow_eval") is True:
            try: row['value']=p.eval()
            except Exception as e: row['evaluation_error']=str(e)
        rows.append(row)
    edges=[]
    for c in node.inputConnections():
        source=c.inputNode(); target=c.outputNode()
        edges.append({"source":source.path() if source else None,"target":target.path() if target else None,
                      "source_output_index":c.outputIndex(),"target_input_index":c.inputIndex()})
    return {"ok":True,"path":path,"node_type":node.type().nameWithCategory(),
            "parameter_count":len(parms),"parameters":rows,
            "next_offset":offset+limit if offset+limit<len(parms) else None,
            "input_names":list(node.inputNames()),"input_labels":list(node.inputLabels()),
            "output_names":list(node.outputNames()),"output_labels":list(node.outputLabels()),
            "input_connections":edges,"last_cook_errors":list(node.errors()),"last_cook_warnings":list(node.warnings()),
            "evaluated_parameters":config.get("allow_eval") is True,
            "explicit_cook_requested":False,"warning":"parm eval can trigger expressions/dependencies; no dynamic menu callbacks were requested"}

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
