"""Cook/read a nominated SOP ONLY with allow_cook=true. Sampling is not whole-geometry QA.
Sources: S-GEO, S-OPNODE. Does not change the current frame or modify geometry.
"""
from __future__ import annotations
from itertools import islice
import math

def run(config: dict) -> dict:
    if config.get("allow_cook") is not True:
        raise ValueError("geometry access can cook expensive upstream networks; set allow_cook=true after review")
    path=config.get("path"); limit=config.get("sample_limit",20)
    if not isinstance(path,str) or not path.startswith("/"):
        raise ValueError("absolute SOP path required")
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1 <= limit <= 500:
        raise ValueError("sample_limit must be 1..500")
    import hou
    node=hou.node(path)
    if node is None or not isinstance(node,hou.SopNode):raise ValueError("path is not a SOP")
    geometry=node.geometry()
    errors=list(node.errors())
    def count(method,intrinsic):
        function=getattr(geometry,method,None)
        return function() if callable(function) else geometry.intrinsicValue(intrinsic)
    counts={"points":count("pointCount","pointcount"),"primitives":count("primCount","primitivecount")}
    attrs={}
    for owner,fn in [("point",geometry.pointAttribs),("vertex",geometry.vertexAttribs),
                     ("primitive",geometry.primAttribs),("detail",geometry.globalAttribs)]:
        attrs[owner]=[{"name":a.name(),"type":str(a.dataType()),"size":a.size()} for a in fn()]
    points=[]; bad=[]
    for p in islice(geometry.iterPoints(),limit):
        pos=list(p.position());finite=all(math.isfinite(v) for v in pos)
        points.append({"number":p.number(),"P":[v if math.isfinite(v) else None for v in pos]})
        if not finite:bad.append(p.number())
    bounds=None
    if counts['points']>0:
        b=geometry.boundingBox()
        values=list(b.minvec())+list(b.maxvec())
        bounds={"min_max":[v if math.isfinite(v) else None for v in values]}
    return {"ok":not errors and not bad,"path":path,"frame":hou.frame(),"counts":counts,
            "bounds":bounds,"attributes":attrs,"point_sample":points,"nonfinite_sample_ids":bad,
            "errors":errors,"warnings":list(node.warnings()),"sampled_points":len(points),
            "sample_scope":"first N points only, not random or exhaustive",
            "semantic_acceptance":"not performed; empty geometry can be intentional"}

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
