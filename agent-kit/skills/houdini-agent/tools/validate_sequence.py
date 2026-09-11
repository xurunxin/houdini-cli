#!/usr/bin/env python3
"""Check sequence names/existence/nonzero size only; does not decode or judge pixels."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import string
import sys

def check(root: Path, pattern: str, start: int, end: int, step: int = 1, min_bytes: int = 1) -> dict:
    if step <= 0 or end < start or min_bytes < 1:
        raise ValueError('invalid range, step, or minimum size')
    if len(range(start,end+1,step)) > 100000:
        raise ValueError('range exceeds 100000 frames')
    fields = [(field,spec,conv) for _,field,spec,conv in string.Formatter().parse(pattern) if field is not None]
    if len(fields) != 1 or fields[0][0] != 'frame' or fields[0][2] is not None:
        raise ValueError('pattern must contain exactly one {frame} or {frame:04d} field')
    if fields[0][1] and not re.fullmatch(r'0?[1-9][0-9]?d|d',fields[0][1]):
        raise ValueError('unsupported frame formatting')
    root=root.resolve(strict=True)
    if not root.is_dir(): raise ValueError('root must be a directory')
    missing=[]; small=[]; total=0; found=0
    for frame in range(start,end+1,step):
        rel=Path(pattern.format(frame=frame))
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('pattern escapes root')
        file=root/rel
        if not file.resolve().is_relative_to(root):
            raise ValueError('symlink escape in sequence path')
        if not file.is_file(): missing.append(frame); continue
        size=file.stat().st_size; found+=1; total+=size
        if size < min_bytes: small.append(frame)
    return {'ok':not missing and not small,'validation':'file-structure-only',
            'expected':len(range(start,end+1,step)), 'found':found,'bytes':total,
            'missing_frames':missing,'undersize_frames':small,'decoded':False,'visual_reviewed':False,
            'warning':'existing non-empty files may be stale, incomplete, undecodable, black or wrong-version; read back and compare manifest'}
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--pattern',required=True)
    p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True)
    p.add_argument('--step',type=int,default=1);p.add_argument('--min-bytes',type=int,default=1)
    a=p.parse_args(argv)
    try:
        report=check(a.root,a.pattern,a.start,a.end,a.step,a.min_bytes)
        print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if report['ok'] else 1
    except (OSError,ValueError) as e:
        print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
