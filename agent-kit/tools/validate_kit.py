#!/usr/bin/env python3
"""Offline structure, local-link, index and Python-syntax checks. NO Houdini execution."""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote,urlparse

def validate(root:Path)->dict:
    root=root.resolve(strict=True);h=root/'skills/houdini-agent';errors=[]
    def load(p):
        try:return json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:errors.append(str(p)+': '+str(e));return {}
    all_json=list(root.rglob('*.json'))
    for p in all_json:load(p)
    registry=load(h/'sources.lock.json');sources=registry.get('sources',[])
    ids=[s.get('id') for s in sources]
    if len(ids)!=len(set(ids)):errors.append('duplicate source IDs')
    known=set(ids)
    for s in sources:
        if urlparse(s.get('url','')).scheme!='https':errors.append('non-HTTPS source: '+str(s.get('id')))
        if not s.get('review_depth') or not s.get('reviewed_on'):errors.append('missing review metadata: '+str(s.get('id')))
        if s.get('pin_kind')=='git-commit' and not re.fullmatch(r'[0-9a-f]{40}',s.get('commit','')):
            errors.append('invalid commit pin: '+str(s.get('id')))
    topics=load(h/'index/topics.json').get('topics',[])
    recipes=load(h/'index/recipes.json').get('recipes',[])
    ids=[d.get('id') for d in topics+recipes]
    if len(ids)!=len(set(ids)):errors.append('duplicate knowledge IDs')
    topic_ids={d['id'] for d in topics}
    for d in topics+recipes:
        path=h/d.get('path','MISSING')
        if not path.is_file():errors.append('missing knowledge page: '+str(path))
        if not (root/'skills'/d.get('skill','MISSING')/'SKILL.md').is_file():errors.append('missing skill for '+str(d.get('id')))
        for k in ('sources','inputs','steps','acceptance','coverage','aliases'):
            if not d.get(k):errors.append('missing field '+k+' in '+str(d.get('id')))
        if not set(d.get('sources',[])).issubset(known):errors.append('unknown source in '+str(d.get('id')))
        if d in recipes and d.get('topic') not in topic_ids:errors.append('unknown parent topic '+str(d.get('id')))
        if path.is_file():
            txt=path.read_text(encoding='utf-8')
            # Synchronization guard for machine-readable canonical records and generated wiki.
            for sentence in d.get('steps',[])+d.get('acceptance',[]):
                if sentence not in txt:errors.append('index/wiki content drift: '+str(d['id']));break
    skill_paths=list((root/'skills').glob('*/SKILL.md'))
    for p in skill_paths:
        text=p.read_text(encoding='utf-8')
        front=re.match(r'^---\n(.*?)\n---\n',text,re.S)
        if not front:errors.append('missing frontmatter: '+str(p));continue
        name=re.search(r'^name:\s*(.+)$',front.group(1),re.M)
        desc=re.search(r'^description:\s*(.+)$',front.group(1),re.M)
        if not name or name.group(1).strip()!=p.parent.name:errors.append('skill name mismatch: '+str(p))
        if not desc or not desc.group(1).strip():errors.append('missing description: '+str(p))
    markdown=list(root.rglob('*.md'));link_count=0
    for p in markdown:
        text=p.read_text(encoding='utf-8')
        text=re.sub(r'```.*?```','',text,flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            if urlparse(target).scheme or target.startswith('#'):continue
            target=unquote(target.split('#')[0])
            if not target:continue
            link_count+=1
            dest=(p.parent/target).resolve()
            if not dest.is_relative_to(root) or not dest.exists():errors.append('broken/local-escaping link: '+str(p.relative_to(root))+' -> '+target)
    python_files=[p for p in root.rglob('*.py') if '__pycache__' not in p.parts]
    for p in python_files:
        try:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        except (SyntaxError,UnicodeError) as e:errors.append(str(e))
    for example in load(h/'index/examples.json').get('examples',[]):
        if not (h/example['path']).is_file():errors.append('missing example '+example['path'])
        if example.get('runtime_tested') is not False:errors.append('runtime evidence must be supplied before changing example status: '+example['path'])
    return {'ok':not errors,'errors':errors,'counts':{'topics':len(topics),'recipes':len(recipes),'skills':len(skill_paths),
             'sources':len(sources),'markdown_files':len(markdown),'json_files':len(all_json),'python_files':len(python_files),'checked_local_links':link_count},
            'scope':'offline structure / local links / index consistency / Python AST; external link liveness and Houdini semantics NOT tested'}
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path)
    a=p.parse_args(argv)
    try:report=validate(a.root)
    except (OSError,ValueError) as e:report={'ok':False,'errors':[str(e)]}
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(text+'\n',encoding='utf-8')
    print(text);return 0 if report['ok'] else 1
if __name__=='__main__':raise SystemExit(main())
