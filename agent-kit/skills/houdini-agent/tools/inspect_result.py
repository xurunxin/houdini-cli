#!/usr/bin/env python3
"""Conservative CLI/MCP/business-result inspection; never an artistic acceptance gate."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

def inspect(payload: object) -> dict:
    errors: list[str] = []
    business_success: list[str] = []
    parse_unknown: list[str] = []
    if not isinstance(payload, dict):
        return {'status': 'unknown', 'errors': [], 'notes': ['expected CLI JSON object'], 'artifact_verified': False}
    if payload.get('ok') is False:
        errors.append('CLI ok=false: '+str(payload.get('error', ''))[:1000])
    def independent_result(obj: object, path: str, depth: int):
        # Each batch item / MCP representation needs its own interpretable outcome.
        before = (len(errors), len(business_success), len(parse_unknown))
        walk(obj, path, depth)
        if before == (len(errors), len(business_success), len(parse_unknown)):
            parse_unknown.append(path+': no recognized business outcome')

    def walk(obj: object, path: str, depth: int = 0):
        if depth > 16:
            parse_unknown.append(path+': nesting limit'); return
        if not isinstance(obj, dict):
            parse_unknown.append(path+': unrecognized result'); return
        if obj.get('isError') is True or obj.get('ok') is False or obj.get('success') is False:
            errors.append(path+': failure flag')
        state = str(obj.get('status', '')).casefold()
        if state in ('error', 'failed', 'failure'):
            errors.append(path+': '+str(obj.get('message', obj.get('error', state)))[:1000])
        elif state and state not in ('success', 'ok', 'completed'):
            parse_unknown.append(path+': unresolved status='+state)
        if obj.get('error') not in (None, '', False, [], {}):
            errors.append(path+': error='+str(obj['error'])[:1000])
        if obj.get('errors'):
            errors.append(path+': errors='+str(obj['errors'])[:1000])
        if obj.get('failed'):
            errors.append(path+': partial failure='+str(obj['failed'])[:1000])
        if obj.get('unsupported'):
            parse_unknown.append(path+': unsupported requested fields='+str(obj['unsupported'])[:1000])
        envelope = 'content' in obj or 'result' in obj or 'structuredContent' in obj or 'results' in obj
        if (obj.get('ok') is True and not envelope) or obj.get('success') is True or state in ('success','ok','completed'):
            business_success.append(path)
        if isinstance(obj.get('validation'), dict):
            walk(obj['validation'],path+'.validation',depth+1)
        if 'structuredContent' in obj:
            independent_result(obj['structuredContent'],path+'.structuredContent',depth+1)
        if 'result' in obj:
            walk(obj['result'],path+'.result',depth+1)
        if 'results' in obj:
            if not isinstance(obj['results'], list) or not obj['results']:
                parse_unknown.append(path+'.results: expected nonempty result array')
            else:
                for i, val in enumerate(obj['results']): independent_result(val,f'{path}.results[{i}]',depth+1)
        if 'content' in obj and (not isinstance(obj['content'], list) or not obj['content']):
            parse_unknown.append(path+'.content: expected nonempty MCP content array')
        if isinstance(obj.get('content'), list):
            for i, item in enumerate(obj['content']):
                if not isinstance(item,dict) or item.get('type') != 'text':
                    parse_unknown.append(f'{path}.content[{i}]: non-text result'); continue
                text = item.get('text','')
                prose_error = isinstance(text,str) and text.strip().lower().startswith(('error:', 'error (', 'connection error', 'server error', 'traceback (', 'failed:'))
                if prose_error:
                    errors.append(f'{path}.content[{i}]: '+text[:1000])
                marker = 'HOUDINI_AGENT_RESULT='
                if isinstance(text,str) and marker in text:
                    if text.count(marker) != 1:
                        parse_unknown.append(f'{path}.content[{i}]: multiple result markers require review')
                        continue
                    # Pinned upstream wraps stdout in prose with literal \n separators.
                    # raw_decode consumes only the JSON object after our explicit marker.
                    try:
                        decoded, end = json.JSONDecoder().raw_decode(text.split(marker,1)[1].lstrip())
                    except (ValueError,TypeError):
                        parse_unknown.append(f'{path}.content[{i}]: invalid result marker')
                    else:
                        independent_result(decoded, f'{path}.content[{i}].agent_result',depth+1)
                        if '--- Stderr ---' in text:
                            parse_unknown.append(f'{path}.content[{i}]: stderr requires review')
                    continue
                try: parsed = json.loads(text)
                except (ValueError,TypeError):
                    # A prose error is strong evidence of failure, never of success.
                    if not prose_error: parse_unknown.append(f'{path}.content[{i}]: free text not interpreted')
                else: independent_result(parsed, f'{path}.content[{i}]',depth+1)
    # Ignore outer ok=true as business proof.
    keys = ['result','results','structuredContent','content']
    if not any(k in payload for k in keys):
        parse_unknown.append('no tool/business result envelope')
    copy = {k:v for k,v in payload.items() if k != 'ok'}
    walk(copy,'$')
    status = 'failed' if errors else ('reported_success' if business_success and not parse_unknown else 'unknown')
    return {'status': status, 'errors': errors, 'business_success_markers': business_success,
            'notes': parse_unknown, 'artifact_verified': False,
            'required_next': 'read back scene/data/files and perform domain acceptance; timeout/interruption => unknown, do not replay'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('file',type=Path)
    a=p.parse_args(argv)
    try:
        result=inspect(json.loads(a.file.read_text(encoding='utf-8-sig')))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return {'reported_success':0,'failed':1,'unknown':3}[result['status']]
    except (OSError,ValueError) as e:
        print(json.dumps({'status':'unknown','error':str(e)},ensure_ascii=False),file=sys.stderr); return 2
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
