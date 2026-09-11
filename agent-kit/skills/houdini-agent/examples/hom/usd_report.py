"""Read nominated LOP stage with explicit cook permission. No editableStage()/USD writes.
Sources: S-LOPNODE and S-SOLARIS. Reports authored direct bindings, NOT resolved bindings.
"""
from __future__ import annotations
from itertools import islice

def run(config:dict)->dict:
    if config.get('allow_cook') is not True:raise ValueError('allow_cook=true required; stage() may cook')
    path=config.get('path');limit=config.get('limit',30)
    if not isinstance(path,str) or not path.startswith('/'):raise ValueError('absolute LOP path required')
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1<=limit<=200:raise ValueError('limit must be 1..200')
    import hou
    node=hou.node(path)
    if node is None or not isinstance(node,hou.LopNode):raise ValueError('path is not a LOP node')
    stage=node.stage(apply_viewport_overrides=False,ignore_errors=False)
    if stage is None:raise ValueError('no stage returned')
    # Read all fields in this one call; do not retain a shared stage for subsequent CLI requests.
    prims=list(islice(stage.Traverse(),limit+1));rows=[]
    for prim in prims[:limit]:
        binding=prim.GetRelationship('material:binding')
        rows.append({'path':str(prim.GetPath()),'type':prim.GetTypeName(),
                     'active':prim.IsActive(),'loaded':prim.IsLoaded(),
                     'direct_material_targets':[str(x) for x in binding.GetTargets()] if binding else []})
    return {'ok':not node.errors(),'node':path,'frame':hou.frame(),'prims':rows,'truncated':len(prims)>limit,
            'meters_per_unit_authored':stage.GetMetadata('metersPerUnit'),
            'up_axis_authored':stage.GetMetadata('upAxis'),'errors':list(node.errors()),
            'scope':'default stage traversal; not an exhaustive audit of inactive/unloaded/instance-proxy prims',
            'binding_warning':'direct relationships only; collection/inherited/stronger binding resolution is NOT checked',
            'note':'no retained stage handles, no writes, no files exported'}

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
