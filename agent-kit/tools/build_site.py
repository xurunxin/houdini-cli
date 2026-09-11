#!/usr/bin/env python3
"""Build one self-contained, offline HTML reader. Uses no external JavaScript or fonts."""
from __future__ import annotations
import argparse
import html
import json
import os
from pathlib import Path
import posixpath
import re
from urllib.parse import quote, unquote, urlsplit


def local_target(current: str, href: str) -> str | None:
    path = unquote(href.split('#', 1)[0])
    if not path:
        return current
    candidate = posixpath.normpath(posixpath.join(posixpath.dirname(current), path))
    if candidate == '..' or candidate.startswith('../') or candidate.startswith('/'):
        return None
    return candidate


def inline(text: str, current: str, known: set[str]) -> str:
    """Small safe Markdown subset. Raw HTML is always escaped, never trusted."""
    pattern = re.compile(r'`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*')
    out = []
    pos = 0
    for match in pattern.finditer(text):
        out.append(html.escape(text[pos:match.start()]))
        if match.group(1) is not None:
            out.append('<code>' + html.escape(match.group(1)) + '</code>')
        elif match.group(2) is not None:
            label, href = match.group(2), match.group(3)
            scheme = urlsplit(href).scheme.lower()
            if scheme in ('https', 'http'):
                out.append(f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)} ↗</a>')
            elif not scheme:
                target = local_target(current, href)
                if target in known:
                    out.append(f'<a href="#doc={quote(target, safe="/")}">{html.escape(label)}</a>')
                else:
                    out.append('<span title="仅在完整知识包中提供">' + html.escape(label) + '</span>')
            else:
                out.append(html.escape(label))
        else:
            out.append('<strong>' + html.escape(match.group(4)) + '</strong>')
        pos = match.end()
    out.append(html.escape(text[pos:]))
    return ''.join(out)


def render_markdown(text: str, current: str, known: set[str]) -> str:
    lines = text.splitlines()
    output = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            language = line[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i += 1
            output.append('<div class="code-label">' + html.escape(language or 'text') + '</div><pre><code>' + html.escape('\n'.join(block)) + '</code></pre>')
            i += 1
            continue
        if line.strip() == '---':
            # SKILL frontmatter is metadata, rendered as a compact definition block.
            if i == 0:
                meta = []; i += 1
                while i < len(lines) and lines[i].strip() != '---':
                    meta.append(lines[i]); i += 1
                output.append('<pre class="frontmatter">' + html.escape('\n'.join(meta)) + '</pre>')
            else:
                output.append('<hr>')
            i += 1
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading:
            level = len(heading.group(1))
            output.append(f'<h{level}>' + inline(heading.group(2), current, known) + f'</h{level}>')
            i += 1
            continue
        if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|\-]+\|\s*$', lines[i + 1]):
            rows = []; i0 = i
            while i < len(lines) and lines[i].startswith('|'):
                if i != i0 + 1:
                    rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            table = ['<div class="table-wrap"><table><thead><tr>']
            table += ['<th>' + inline(cell, current, known) + '</th>' for cell in rows[0]]
            table += ['</tr></thead><tbody>']
            for row in rows[1:]:
                table += ['<tr>'] + ['<td>' + inline(c, current, known) + '</td>' for c in row] + ['</tr>']
            table += ['</tbody></table></div>']
            output.append(''.join(table))
            continue
        item = re.match(r'^(?:([-*])|(\d+)\.)\s+(.+)$', line)
        if item:
            ordered = item.group(2) is not None
            tag = 'ol' if ordered else 'ul'
            block = [f'<{tag}>']
            while i < len(lines):
                item = re.match(r'^(?:([-*])|(\d+)\.)\s+(.+)$', lines[i])
                if not item or (item.group(2) is not None) != ordered:
                    break
                block.append('<li>' + inline(item.group(3), current, known) + '</li>')
                i += 1
            block.append(f'</{tag}>'); output.append(''.join(block))
            continue
        if line.startswith('>'):
            output.append('<blockquote>' + inline(line.lstrip('> '), current, known) + '</blockquote>')
            i += 1
            continue
        paragraph = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||>|[-*] |\d+\. )', lines[i]):
            paragraph.append(lines[i]); i += 1
        output.append('<p>' + '<br>'.join(inline(x, current, known) for x in paragraph) + '</p>')
    return '\n'.join(output)


def collect(root: Path) -> list[dict]:
    hub = root / 'skills/houdini-agent'
    topics = json.loads((hub / 'index/topics.json').read_text(encoding='utf-8'))['topics']
    recipes = json.loads((hub / 'index/recipes.json').read_text(encoding='utf-8'))['recipes']
    by_path = {'skills/houdini-agent/' + d['path']: d for d in topics + recipes}
    paths = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix in ('.md', '.json', '.py', '.vfl') and '__pycache__' not in p.parts and 'validation' not in p.relative_to(root).parts and 'tests' not in p.relative_to(root).parts)
    known = {p.relative_to(root).as_posix() for p in paths}
    known.update(('LICENSE', 'wiki.html'))
    documents = []
    paths += [root / 'LICENSE']
    for p in paths:
        relative = p.relative_to(root).as_posix()
        text = p.read_text(encoding='utf-8')
        d = by_path.get(relative)
        title = d['title'] if d else next((x.lstrip('# ').strip() for x in text.splitlines() if x.startswith('# ')), p.name)
        if d:
            kind = 'recipe' if d['id'].startswith('recipe-') else 'topic'
        elif p.name == 'SKILL.md':
            kind = 'skill'; title = p.parent.name
        elif 'examples' in p.parts:
            kind = 'example'
        elif p.suffix in ('.json', '.py', '.vfl'):
            kind = 'data'
        else:
            kind = 'guide'
        rendered = render_markdown(text, relative, known) if p.suffix == '.md' else '<h1>' + html.escape(title) + '</h1><pre><code>' + html.escape(text) + '</code></pre>'
        documents.append({'path': relative, 'title': title, 'kind': kind, 'coverage': d.get('coverage', '') if d else '',
                          'aliases': ' '.join(d.get('aliases', [])) if d else '', 'html': rendered, 'text': text})
    # Put the entrypoints first; stable source ordering after them.
    priorities = {'README.md': 0, 'skills/houdini-agent/wiki/quickstart.md': 1, 'skills/houdini-agent/wiki/README.md': 2}
    return sorted(documents, key=lambda d: (priorities.get(d['path'], 3), d['path']))


TEMPLATE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'">
<title>Houdini Agent Wiki · 离线知识库</title>
<style>
:root{--ink:#172a34;--muted:#637781;--line:#dce5e7;--accent:#087e80;--paper:#f4f7f7;--nav:#112d36;--soft:#eaf4f3}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei","Noto Sans CJK SC",sans-serif}
button,input,select{font:inherit}button,a,input,select{outline-offset:4px}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.shell{display:grid;grid-template-columns:342px minmax(0,1fr);min-height:100vh}aside{background:var(--nav);color:#e7f4f4;position:sticky;top:0;height:100vh;display:flex;flex-direction:column;padding:28px 22px 14px;border-right:1px solid #29434a}
.brand{letter-spacing:.17em;color:#80cbcb;font-size:11px;font-weight:700}.brand-title{font-size:24px;font-weight:700;margin:7px 0 2px;letter-spacing:-.03em}.brand-sub{font-size:12px;color:#a8c1c8;margin-bottom:22px}.search-label{font-size:12px;color:#b5cbd0}
#search{margin-top:7px;width:100%;padding:11px 13px;border-radius:7px;border:1px solid #45606a;color:#f3fafb;background:#1d3b45}#search::placeholder{color:#99b2b9}#search:focus{outline:2px solid #72c5c5}
.search-row{display:flex;gap:8px;margin:10px 0 6px;align-items:center}#kind{background:#1d3b45;color:#dcebed;padding:6px 8px;border:1px solid #45606a;border-radius:5px;max-width:150px}#result-count{font-size:11px;color:#9db8bf;margin-left:auto}
#results{overflow:auto;margin:10px -8px 0;padding:0 7px 12px;flex:1;scrollbar-width:thin;scrollbar-color:#49656e transparent}.result{display:block;color:#cfdee2;padding:11px 12px;border:1px solid transparent;border-radius:7px;margin-bottom:3px;line-height:1.45}.result:hover{background:#1f424d;text-decoration:none}.result.active{background:#234b52;border-color:#488084;color:#fff}.result-title{font-size:13px;display:block}.result-meta{font-size:10px;color:#95b5bc;display:block;margin-top:4px}.nav-foot{font-size:10px;color:#9ab5bd;padding-top:10px;border-top:1px solid #304b54}kbd{font:11px monospace;border:1px solid #49666f;padding:1px 4px;border-radius:3px}
main{padding:30px 46px 70px;min-width:0;max-width:1250px;width:100%;margin:auto}.topline{display:flex;justify-content:space-between;align-items:center;gap:16px;border-bottom:1px solid var(--line);padding-bottom:18px;color:var(--muted);font-size:12px}.status{color:#916423;border:1px solid #e3cfad;background:#fbf5e9;border-radius:30px;padding:4px 11px}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:23px 0}.metric{padding:14px 17px;background:#fff;border:1px solid var(--line);border-radius:8px}.metric strong{display:block;font-size:25px;font-weight:650;letter-spacing:-.04em;line-height:1.35}.metric span{font-size:11px;color:var(--muted)}
.pathbar{display:flex;gap:12px;align-items:center;margin:24px 0 12px;font-size:11px;color:var(--muted)}#path{flex:1;word-break:break-all}#copy{background:#fff;border:1px solid var(--line);border-radius:5px;padding:5px 10px;cursor:pointer;color:var(--muted);white-space:nowrap}#copy:hover{color:var(--accent);border-color:var(--accent)}#copy-status{font-size:11px;color:var(--accent);min-height:18px}
article{background:#fff;border:1px solid var(--line);border-radius:11px;padding:33px 40px;box-shadow:0 5px 20px #19313c05;overflow-wrap:anywhere;min-height:300px}article h1{font-size:29px;line-height:1.4;letter-spacing:-.025em;margin:0 0 18px;font-weight:700}article h2{font-size:19px;line-height:1.5;margin:32px 0 12px;padding-top:20px;border-top:1px solid #e8eeee}article h3{font-size:16px;margin-top:25px}article p{margin:12px 0}article ul,article ol{padding-left:24px}article li{margin:7px 0}article code{font:12.5px/1.7 Consolas,"SFMono-Regular",monospace;background:#eef4f4;padding:2px 5px;border-radius:4px;word-break:break-word}article pre{background:#142e38;color:#e1f0f1;padding:18px 20px;border-radius:0 0 6px 6px;overflow:auto;line-height:1.6;margin:0 0 20px;white-space:pre;overflow-wrap:normal}article pre code{background:none;color:inherit;padding:0;word-break:normal}.code-label{margin-top:16px;padding:7px 20px;background:#244650;color:#a5c5cc;font:10px/1.5 monospace;border-radius:6px 6px 0 0;text-transform:uppercase;letter-spacing:.1em}article pre.frontmatter{font-size:11px;background:#edf4f4;color:#45636e;border-radius:6px;white-space:pre-wrap;margin-bottom:20px}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:12px;line-height:1.65}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{background:var(--soft);font-weight:600;white-space:nowrap}blockquote{margin:15px 0;padding:12px 20px;background:#eef7f5;border-left:3px solid var(--accent)}.empty{padding:30px 10px;color:#a9c5cb}footer{font-size:11px;color:var(--muted);margin-top:20px}.hide{display:none}
@media(max-width:1000px){.shell{grid-template-columns:290px minmax(0,1fr)}aside{padding:22px 16px}main{padding:25px 25px 50px}article{padding:27px}article h1{font-size:25px}.metric{padding:12px}.metric strong{font-size:22px}}
@media(max-width:700px){.shell{display:block}aside{position:relative;height:auto;padding:20px}#results{max-height:250px}.brand-sub{margin-bottom:10px}.nav-foot{display:none}main{padding:20px 15px 45px}.metrics{gap:6px;margin:17px 0}.metric{padding:10px}.metric strong{font-size:21px}.metric span{font-size:10px}.topline{font-size:10px;gap:6px}.status{padding:3px 8px}article{padding:23px 20px}article h1{font-size:24px}}
@media print{aside,.metrics,.topline,.pathbar,#copy-status,footer{display:none}.shell{display:block}main{max-width:none;padding:0}article{border:0;box-shadow:none;padding:0}article pre{white-space:pre-wrap;background:#f3f3f3;color:#111}article h2{break-after:avoid}.table-wrap{overflow:visible}}
</style></head><body>
<div class="shell"><aside aria-label="知识目录"><div class="brand">PROCEDURAL · AGENT KNOWLEDGE</div><div class="brand-title">Houdini Agent Wiki</div><div class="brand-sub">可检索的知识 · 有边界的执行</div>
<label class="search-label" for="search">查效果、故障、节点或工作流</label><input id="search" type="search" placeholder="布料穿透 / USD / 烟不显示" autocomplete="off">
<div class="search-row"><select id="kind" aria-label="筛选条目类型"><option value="all">全部类型</option><option value="topic">领域知识</option><option value="recipe">任务配方</option><option value="skill">Agent Skills</option><option value="guide">操作与维护</option><option value="example">代码示例</option><option value="data">工具与索引</option></select><span id="result-count" aria-live="polite"></span></div><nav id="results" aria-label="检索结果"></nav>
<div class="nav-foot"><kbd>/</kbd> 聚焦检索　·　纯离线，无外部请求<br>v0.1.0 / 2026-09-11</div></aside>
<main><div class="topline"><span>HOUDINI-CLI 0.2.0 · KNOWLEDGE KIT</span><span class="status">Houdini 现场验收待执行</span></div>
<div class="metrics"><div class="metric"><strong>32</strong><span>领域知识卡</span></div><div class="metric"><strong>40</strong><span>任务配方</span></div><div class="metric"><strong>20</strong><span>Agent Skills</span></div><div class="metric"><strong>81</strong><span>分级来源记录</span></div></div>
<div class="pathbar"><span id="path"></span><button id="copy" type="button">复制原文</button></div><div id="copy-status" role="status"></div><article id="article" aria-label="知识正文"></article>
<footer>原理与操作建议不等于运行证据。当前工具与参数以现场 schema 为准；代码未在 Houdini 中实测。外部参考链接需联网。</footer></main></div>
<script type="application/json" id="documents">__DOCUMENTS__</script>
<script>
'use strict';
const docs=JSON.parse(document.getElementById('documents').textContent);
const byPath=new Map(docs.map(d=>[d.path,d]));
const labels={topic:'领域知识',recipe:'任务配方',skill:'Agent Skill',guide:'操作与维护',example:'代码示例',data:'工具与索引'};
const search=document.getElementById('search'),kind=document.getElementById('kind'),results=document.getElementById('results');
let current='README.md';
const normalized=s=>s.toLowerCase().replace(/\s+/g,' ').trim();
for(const d of docs){d.searchTitle=normalized(d.title+' '+d.aliases);d.searchText=normalized(d.text);}
function score(d,q){if(!q)return 1;let value=0;if(d.searchTitle.includes(q))value+=60;if(d.searchText.includes(q))value+=8;const parts=q.split(' ').filter(Boolean);for(const t of parts){if(d.searchTitle.includes(t))value+=15;if(d.searchText.includes(t))value+=2;}if(!value&&q.length>2&&/[\u3400-\u9fff]/.test(q)){for(let i=0;i<q.length-1;i++){const t=q.slice(i,i+2);if(d.searchTitle.includes(t))value+=3;if(d.searchText.includes(t))value+=.2;}}return value;}
function list(){const q=normalized(search.value);const found=docs.filter(d=>kind.value==='all'||d.kind===kind.value).map((d,i)=>({d,i,s:score(d,q)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s||a.i-b.i);results.replaceChildren();document.getElementById('result-count').textContent=found.length+' 条';for(const {d} of found){const a=document.createElement('a');a.href='#doc='+encodeURIComponent(d.path);a.className='result'+(d.path===current?' active':'');if(d.path===current)a.setAttribute('aria-current','page');const title=document.createElement('span');title.className='result-title';title.textContent=d.title;const meta=document.createElement('span');meta.className='result-meta';meta.textContent=labels[d.kind]+(d.coverage==='discovery'?' · 导航级':'');a.append(title,meta);results.append(a);}if(!found.length){const p=document.createElement('p');p.className='empty';p.textContent='没有匹配条目。可改用更短的关键词或切换类型。';results.append(p);}}
function route(){let p='README.md';try{if(location.hash.startsWith('#doc='))p=decodeURIComponent(location.hash.slice(5));}catch(e){p='README.md';}if(p==='wiki.html')p='README.md';const d=byPath.get(p);if(!d){document.getElementById('article').textContent='未找到此条目。请从左侧目录重新选择。';return;}current=p;document.getElementById('path').textContent=p;document.getElementById('article').innerHTML=d.html;document.getElementById('copy-status').textContent='';document.title=d.title+' · Houdini Agent Wiki';list();}
search.addEventListener('input',list);kind.addEventListener('change',list);window.addEventListener('hashchange',route);document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();search.focus();}});
document.getElementById('copy').addEventListener('click',async()=>{const d=byPath.get(current);try{if(!navigator.clipboard)throw new Error('clipboard unavailable');await navigator.clipboard.writeText(d.text);document.getElementById('copy-status').textContent='原始 Markdown / 代码已复制。';}catch(e){document.getElementById('copy-status').textContent='浏览器未授权剪贴板；可选中正文复制，或从完整知识包读取原文件。';}});
route();
</script></body></html>'''


def build(root: Path, output: Path) -> dict:
    root = root.resolve(strict=True)
    documents = collect(root)
    payload = json.dumps(documents, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    page = TEMPLATE.replace('__DOCUMENTS__', payload)
    if output.is_symlink():
        raise ValueError('Refusing to replace symlink output')
    output.write_text(page, encoding='utf-8')
    return {'ok': True, 'output': str(output), 'embedded_documents': len(documents), 'bytes': output.stat().st_size,
            'runtime_testing': 'not performed; reader contains existing evidence boundaries'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--output', type=Path)
    a = p.parse_args(argv)
    try:
        report = build(a.root, a.output or a.root / 'wiki.html')
    except (OSError, ValueError, KeyError, TypeError) as e:
        report = {'ok': False, 'error': str(e)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
