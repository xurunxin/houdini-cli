"""Create a tiny independent graph in /obj/AGENT_<task>. No delete/reset/save/render.
Requires allow_write=true AND allow_cook=true; task token restricted; fails on name conflict.
Only meant to smoke-test basic graph mechanics, not a reusable production builder.
Sources: S-NODE, S-OPNODE, S-BOX, S-XFORM, S-GEO.
"""
from __future__ import annotations
import math
import re

def validate_config(config:dict)->tuple[str,list[float],list[float]]:
    if config.get("allow_write") is not True or config.get("allow_cook") is not True:
        raise ValueError("explicit allow_write=true and allow_cook=true required")
    task=config.get("task","")
    if not isinstance(task,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,39}',task):
        raise ValueError("task must match [A-Za-z][A-Za-z0-9_]{0,39}")
    def vector(name,default,positive=False):
        value=config.get(name,default)
        if not isinstance(value,(list,tuple)) or len(value)!=3:
            raise ValueError(name+" must have 3 values")
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in value):
            raise ValueError(name+" must have finite numeric values")
        result=list(map(float,value))
        if positive and any(x<=0 or x>1000 for x in result):raise ValueError(name+" requires 0 < x <= 1000")
        if any(abs(x)>1e6 for x in result):raise ValueError(name+" outside smoke-test bounds")
        return result
    return task,vector('size',[1,1,1],True),vector('translate',[0,1,0])

def run(config:dict)->dict:
    task,size,translate=validate_config(config)
    import hou
    parent=hou.node('/obj'); name='AGENT_'+task
    if parent is None:raise ValueError('/obj missing')
    if parent.node(name) is not None:
        raise ValueError('name already exists; inspect '+parent.path()+'/'+name+'; never retry by auto-numbering/deleting')
    # Preflight exact installed types before any writes. Parameters verified after instantiation.
    for category,type_name in [(hou.objNodeTypeCategory(),'geo'),(hou.sopNodeTypeCategory(),'box'),
                              (hou.sopNodeTypeCategory(),'xform'),(hou.sopNodeTypeCategory(),'null')]:
        if category.nodeTypes().get(type_name) is None:raise ValueError('required exact type absent: '+type_name)
    container=parent.createNode('geo',node_name=name,run_init_scripts=False,exact_type_name=True)
    container.setUserData('houdini_agent_task',task)
    container.setUserData('houdini_agent_recipe','basic-sop-smoke-v1')
    box=container.createNode('box',node_name='SOURCE_BOX',exact_type_name=True)
    transform=container.createNode('xform',node_name='MOVE',exact_type_name=True)
    output=container.createNode('null',node_name='OUT',exact_type_name=True)
    size_parm=box.parmTuple('size'); move_parm=transform.parmTuple('t')
    if size_parm is None or move_parm is None or len(size_parm)!=3 or len(move_parm)!=3:
        raise ValueError('unexpected live parameter schema; graph retained for inspection: '+container.path())
    size_parm.set(size);move_parm.set(translate)
    transform.setInput(0,box);output.setInput(0,transform)
    output.setDisplayFlag(True);output.setRenderFlag(True);container.layoutChildren()
    output.cook(force=True)
    geo=output.geometry();errors=list(output.errors());bounds=geo.boundingBox()
    expected_min=[t-s/2 for t,s in zip(translate,size)];expected_max=[t+s/2 for t,s in zip(translate,size)]
    actual_min=list(bounds.minvec());actual_max=list(bounds.maxvec())
    matches=all(abs(a-b)<1e-5 for a,b in zip(actual_min+actual_max,expected_min+expected_max))
    return {"ok":not errors and matches,"created_root":container.path(),"output":output.path(),
            "frame":hou.frame(),"bounds":{"min":actual_min,"max":actual_max},"bbox_matches":matches,
            "errors":errors,"saved":False,"rendered":False,
            "note":"graph remains in the unsaved scene; do not rerun same task after timeout; inspect it"}

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
