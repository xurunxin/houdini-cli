#!/usr/bin/env python3
"""Deterministic offline task lookup. No network, embeddings, or Houdini required."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re
import sys

HUB = Path(__file__).resolve().parents[1]

def load_index(hub: Path = HUB) -> tuple[list[dict], dict[str, dict]]:
    topics = json.loads((hub / 'index/topics.json').read_text(encoding='utf-8'))['topics']
    recipes_path = hub / 'index/recipes.json'
    recipes = json.loads(recipes_path.read_text(encoding='utf-8'))['recipes'] if recipes_path.exists() else []
    docs = [dict(t, kind='topic') for t in topics] + [dict(r, kind='recipe') for r in recipes]
    sources = json.loads((hub / 'sources.lock.json').read_text(encoding='utf-8'))['sources']
    return docs, {s['id']: s for s in sources}

def tokens(text: str) -> set[str]:
    text = text.casefold()
    result = set(re.findall(r'[a-z0-9_]+', text))
    for run in re.findall(r'[\u3400-\u9fff]+', text):
        if len(run) == 1:
            result.add(run)
        else:
            result.update(run[i:i+2] for i in range(len(run)-1))
    return result

def field_text(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)

def search(query: str, documents: list[dict], limit: int = 5, kind: str = 'all') -> list[dict]:
    q = query.strip().casefold()
    if not q:
        return []
    terms = tokens(q)
    frequency = {term: sum(term in tokens(field_text(d)) for d in documents) for term in terms}
    weights = {'id': 7, 'title': 7, 'aliases': 9, 'node_candidates': 6,
               'goal': 4, 'inputs': 2, 'steps': 1, 'troubleshooting': 3}
    ranked = []
    for d in documents:
        if kind != 'all' and d['kind'] != kind:
            continue
        score = 0.0
        for field, weight in weights.items():
            val = field_text(d.get(field, ''))
            ft = tokens(val)
            score += weight * sum(1 + math.log((1 + len(documents)) / (1 + frequency[t]))
                                  for t in terms & ft)
        for alias in [d['id'], d['title'], *d.get('aliases', [])]:
            a = alias.casefold()
            if len(a) >= 2 and a in q:
                score += 25 + 2 * min(len(a), 12)
        if score > 0:
            ranked.append(dict(d, score=round(score, 3)))
    return sorted(ranked, key=lambda d: (-d['score'], d['kind'], d['id']))[:limit]

def compact(d: dict, sources: dict[str, dict]) -> dict:
    return {k: d.get(k) for k in ('kind', 'id', 'title', 'path', 'skill', 'coverage', 'score')} | {
        'goal': d.get('goal', ''),
        'next_step': d.get('steps', [''])[0],
        'acceptance': d.get('acceptance', [])[:2],
        'sources': [{'id': i, 'url': sources[i]['url']} for i in d.get('sources', [])],
        'runtime_tested': False,
    }

def bounded_payload(payload: dict, max_chars: int) -> str:
    """Bound complete JSON, never cut inside a string. Budget is characters, not tokens."""
    def encode():
        return json.dumps(payload, ensure_ascii=False, indent=2)
    text = encode()
    while len(text) > max_chars and payload.get('results'):
        last = payload['results'][-1]
        if last.get('sources'):
            last['sources'] = []
        elif last.get('acceptance'):
            last['acceptance'] = []
        elif last.get('next_step'):
            last['next_step'] = ''
        elif last.get('goal'):
            last['goal'] = ''
        else:
            payload['results'].pop()
        payload['truncated'] = True
        text = encode()
    return text

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('search'); p.add_argument('query'); p.add_argument('--kind', choices=['all','topic','recipe'], default='all')
    p.add_argument('--limit', type=int, default=5); p.add_argument('--max-chars', type=int, default=10000)
    p = sub.add_parser('show'); p.add_argument('id')
    p = sub.add_parser('sources'); p.add_argument('id', nargs='?')
    sub.add_parser('list')
    args = parser.parse_args(argv)
    try:
        documents, sources = load_index()
        if args.command == 'search':
            if len(args.query) > 2000:
                raise ValueError('query must be at most 2000 characters')
            if not 1 <= args.limit <= 30 or not 1024 <= args.max_chars <= 100000:
                raise ValueError('limit must be 1..30 and max-chars 1024..100000')
            result = search(args.query, documents, args.limit, args.kind)
            data = {'ok': True, 'query': args.query[:256], 'budget_unit': 'unicode_characters',
                    'truncated': False, 'results': [compact(d, sources) for d in result],
                    'hint': 'paths are relative to this skill; no matches => use matched-version official Help, then live node/schema discovery'}
            print(bounded_payload(data, args.max_chars))
        elif args.command == 'show':
            hits = [d for d in documents if d['id'] == args.id]
            if not hits:
                raise ValueError(f'unknown id: {args.id}')
            print(json.dumps(hits[0], ensure_ascii=False, indent=2))
        elif args.command == 'sources':
            if args.id and args.id not in sources:
                raise ValueError(f'unknown source: {args.id}')
            print(json.dumps(sources[args.id] if args.id else list(sources.values()), ensure_ascii=False, indent=2))
        else:
            print(json.dumps([{k: d.get(k) for k in ('kind','id','title','path','skill','coverage')} for d in documents], ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
