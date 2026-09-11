#!/usr/bin/env python3
"""Install this additive knowledge pack into an existing project. No global config edits."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import uuid
ROOT=Path(__file__).resolve().parents[1]

def unsafe_link(p:Path)->bool:
    if p.is_symlink():return True
    if hasattr(p,'is_junction') and p.is_junction():return True
    try:
        info=p.lstat()
        return bool(getattr(info,'st_file_attributes',0) & getattr(stat,'FILE_ATTRIBUTE_REPARSE_POINT',0x400))
    except FileNotFoundError:return False

def safe_path(root:Path,path:Path)->None:
    if not path.is_relative_to(root):raise ValueError(f'path outside target: {path}')
    current=root
    for part in path.relative_to(root).parts:
        current=current/part
        if unsafe_link(current):raise ValueError(f'symlink/junction/reparse point rejected: {current}')
    if not path.resolve().is_relative_to(root):raise ValueError(f'resolved path escapes target: {path}')

def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def make_plan(source:Path,target:Path,agent:str='codex',profile:str='core',force:bool=False)->list[dict]:
    if agent not in ('codex','claude','all') or profile not in ('core','all'):
        raise ValueError('invalid agent or profile')
    if unsafe_link(target):raise ValueError('target itself must not be a symlink/junction')
    target=target.resolve(strict=True)
    if not target.is_dir():raise ValueError('target must be an existing project directory')
    skills=source/'skills'
    directories=['.agents','.claude'] if agent=='all' else ['.claude' if agent=='claude' else '.agents']
    names=['houdini-agent'] if profile=='core' else sorted(p.name for p in skills.iterdir() if p.is_dir())
    plan=[]
    for name in names:
        folder=skills/name
        if unsafe_link(folder) or not (folder/'SKILL.md').is_file():raise ValueError(f'invalid skill source: {name}')
        for src in sorted(folder.rglob('*')):
            if unsafe_link(src):raise ValueError(f'unsafe source link: {src}')
            if '__pycache__' in src.parts or src.suffix=='.pyc' or not src.is_file():continue
            for directory in directories:
                dest=target/directory/'skills'/name/src.relative_to(folder)
                safe_path(target,dest)
                if dest.exists() and not dest.is_file():raise ValueError(f'target is not a regular file: {dest}')
                old=sha(dest) if dest.exists() else None
                new=sha(src)
                status='unchanged' if old==new else ('update' if old else 'install')
                if status=='update' and not force:raise ValueError(f'custom/existing file conflict: {dest}; review before --force (backs up modified files)')
                plan.append({'source':str(src),'destination':str(dest),'old_sha256':old,'new_sha256':new,'status':status})
    return plan

def install(source:Path,target:Path,agent:str='codex',profile:str='core',force:bool=False,dry_run:bool=False)->dict:
    plan=make_plan(source,target,agent,profile,force)
    root=target.resolve(strict=True)
    run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    backup=root/'.houdini-agent-kit-backups'/run
    completed=[]
    if not dry_run:
        try:
            for item in plan:
                if item['status']=='unchanged':continue
                dst=Path(item['destination']);src=Path(item['source']);safe_path(root,dst)
                now=sha(dst) if dst.is_file() else None
                if now!=item['old_sha256']:raise ValueError(f'target changed after preflight: {dst}')
                if sha(src)!=item['new_sha256']:raise ValueError(f'source changed after preflight: {src}')
                if item['status']=='update':
                    saved=backup/dst.relative_to(root);safe_path(root,saved)
                    saved.parent.mkdir(parents=True,exist_ok=True)
                    with saved.open('xb') as out:out.write(dst.read_bytes())
                dst.parent.mkdir(parents=True,exist_ok=True);safe_path(root,dst)
                tmp=dst.with_name(dst.name+'.'+uuid.uuid4().hex+'.tmp')
                try:
                    with tmp.open('xb') as out:out.write(src.read_bytes())
                    # Recheck before replacement; no claim of adversarial race-proof sandboxing.
                    safe_path(root,dst)
                    if (sha(dst) if dst.is_file() else None)!=item['old_sha256']:
                        raise ValueError(f'target changed during write: {dst}')
                    os.replace(tmp,dst)
                finally:
                    if tmp.exists():tmp.unlink()
                completed.append(str(dst))
        except Exception as error:
            raise RuntimeError(json.dumps({'error':str(error),'completed':completed,'backup':str(backup) if backup.exists() else None,
                                           'note':'per-file atomic, not whole-install transactional; no automatic rollback'},ensure_ascii=False)) from error
    return {'ok':True,'project':str(root),'agent':agent,'profile':profile,'dry_run':dry_run,
            'counts':{s:sum(i['status']==s for i in plan) for s in ('install','update','unchanged')},
            'backup':str(backup) if backup.exists() else None,'plan':plan}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target',type=Path,required=True);p.add_argument('--agent',choices=['codex','claude','all'],default='codex')
    p.add_argument('--profile',choices=['core','all'],default='core');p.add_argument('--dry-run',action='store_true');p.add_argument('--force',action='store_true')
    a=p.parse_args(argv)
    try:
        report=install(ROOT,a.target,a.agent,a.profile,a.force,a.dry_run)
        print(json.dumps(report,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,RuntimeError) as e:
        print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
