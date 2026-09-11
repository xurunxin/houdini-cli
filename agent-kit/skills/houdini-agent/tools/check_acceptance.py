#!/usr/bin/env python3
"""Validate an evidence manifest. File presence is NOT proof its semantic claims are true."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import sys

def check(report:dict,base:Path)->dict:
    if not isinstance(report,dict) or not report.get('task') or not isinstance(report.get('checks'),list) or not report['checks']:
        raise ValueError('task and nonempty checks are required')
    base=base.resolve(strict=True);counts={s:0 for s in ('pass','fail','unknown','not_applicable')};errors=[]
    for i,item in enumerate(report['checks']):
        if not isinstance(item,dict):errors.append(f'checks[{i}] is not an object');continue
        state=item.get('status')
        if state not in counts:errors.append(f'checks[{i}] invalid status');continue
        counts[state]+=1
        if not item.get('criterion') or item.get('layer') not in ('technical','temporal','visual'):
            errors.append(f'checks[{i}] requires criterion and valid layer')
        evidence=item.get('evidence',[])
        if not isinstance(evidence,list):errors.append(f'checks[{i}] evidence must be an array');continue
        if state=='pass' and not evidence:errors.append(f'checks[{i}] pass requires evidence')
        if state=='not_applicable' and not item.get('reason'):errors.append(f'checks[{i}] not_applicable requires reason')
        for e in evidence:
            if not isinstance(e,dict) or not isinstance(e.get('path'),str):errors.append(f'checks[{i}] malformed evidence');continue
            relative=Path(e['path'])
            if relative.is_absolute() or '..' in relative.parts:errors.append(f'checks[{i}] evidence path must stay under base');continue
            path=(base/relative).resolve()
            if not path.is_relative_to(base) or not path.is_file():errors.append(f'checks[{i}] missing/escaping evidence: {e["path"]}')
            if not e.get('observed'):errors.append(f'checks[{i}] evidence requires a concrete observed statement')
    state='invalid' if errors else 'fail' if counts['fail'] else 'unknown' if counts['unknown'] else 'reported_pass'
    return {'status':state,'counts':counts,'errors':errors,'semantic_verified':False,
            'note':'manifest structure and evidence file presence only; no image/video/Houdini interpretation performed'}
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--base',type=Path,required=True);a=p.parse_args(argv)
    try:
        result=check(json.loads(a.manifest.read_text(encoding='utf-8-sig')),a.base)
        print(json.dumps(result,ensure_ascii=False,indent=2));return {'reported_pass':0,'fail':1,'invalid':2,'unknown':3}[result['status']]
    except (OSError,ValueError) as e:
        print(json.dumps({'status':'invalid','error':str(e)},ensure_ascii=False),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
