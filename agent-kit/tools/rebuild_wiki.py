#!/usr/bin/env python3
"""Rebuild only generated topic/recipe pages and Wiki indices from canonical JSON."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import tempfile


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def safe_destination(root: Path, relative: str) -> Path:
    logical = PurePosixPath(relative)
    if logical.is_absolute() or '..' in logical.parts or '\\' in relative:
        raise ValueError(f'Unsafe generated path: {relative}')
    current = root
    for part in logical.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Symlink in generated path: {current}')
        if current.exists() and getattr(current.lstat(), 'st_file_attributes', 0) & 0x400:
            raise ValueError(f'Reparse point in generated path: {current}')
    if not current.resolve().is_relative_to(root):
        raise ValueError(f'Path escapes source root: {relative}')
    return current


def source_lines(ids, sources, detailed=False):
    result = []
    for sid in ids:
        s = sources[sid]
        suffix = f" — {s['review_depth']}；" if detailed else ''
        result.append(f"- [{sid} · {s['title']}]({s['url']}){suffix}")
    return '\n'.join(result)


def render_topic(d, source_map, reviewed, cli_path, acceptance_path):
    lines = [f"# {d['title']}", '',
             f"ID: `{d['id']}` · 领域: {' / '.join(d['contexts'])} · Skill: `{d['skill']}`",
             f"覆盖等级: **{d['coverage']}** · 来源复核: {reviewed} · **目标 Houdini 运行验收：未执行**", '',
             '## 适用目标', d['goal'], '', '## 输入契约', d['inputs'], '', '## 推荐操作']
    lines += [f'{i}. {x}' for i, x in enumerate(d['steps'], 1)]
    lines += ['', '## 验收条件'] + ['- ' + x for x in d['acceptance']]
    lines += ['', '## 症状 → 优先检查']
    lines += [f'**{symptom}**：{check}' for symptom, check in d.get('troubleshooting', [])]
    lines += ['', '## 版本与边界', d.get('version_note', '现场版本、节点全名和参数 schema 为准。'), '',
              '节点/工具候选（检索词，不是保证可调用的内部类型名）：' + '、'.join(f'`{x}`' for x in d['node_candidates']), '',
              f'统一执行协议见 [CLI 契约]({cli_path})；验收分层见 [验收卡]({acceptance_path})。', '',
              '## 来源与进一步查询', source_lines(d['sources'], source_map, True), '',
              '以上推荐步骤、排错顺序和验收清单为本包编写；不是源站逐字翻译。']
    return '\n'.join(lines) + '\n'


def render_recipe(d, topics, source_map):
    topic = topics[d['topic']]
    parent = os.path.relpath(topic['path'], str(PurePosixPath(d['path']).parent)).replace(os.sep, '/')
    cli = os.path.relpath(topics['cli-contract']['path'], str(PurePosixPath(d['path']).parent)).replace(os.sep, '/')
    lines = [f"# {d['title']}", '', f"ID: `{d['id']}` · Skill: `{d['skill']}` · **{d['coverage']}**", '',
             '## 输入', d['inputs'], '', '## 最小网络意图', f"`{d['minimum_network']}`", '',
             '**这是概念数据流，不是可直接执行的节点类型/端口列表。** 先发现现场节点全名及输入标签，再转换为操作计划。', '',
             '## 必须现场查询的参数/契约', '、'.join(d['parameters_to_discover']), '', '## 执行']
    lines += [f'{i}. {x}' for i, x in enumerate(d['steps'], 1)]
    lines += ['', '## 验收'] + ['- ' + x for x in d['acceptance']]
    lines += ['', f"风险: `{d['risk']}`。只在已授权路径与任务命名空间执行；不重放超时未知操作。", '',
              f'进一步阅读：[领域卡]({parent}) · [执行协议]({cli})']
    if d.get('example'):
        example = os.path.relpath(d['example'], str(PurePosixPath(d['path']).parent)).replace(os.sep, '/')
        lines += ['', f'[配套示例]({example})：先读文件中的前提、配置和运行边界；未在目标 Houdini 执行。']
    lines += ['', '## 来源', source_lines(d['sources'], source_map)]
    return '\n'.join(lines) + '\n'


def generated_files(root: Path) -> dict[str, str]:
    h = root / 'skills/houdini-agent'
    registry = load(h / 'sources.lock.json')
    sources = {x['id']: x for x in registry['sources']}
    topics = load(h / 'index/topics.json')['topics']
    recipes = load(h / 'index/recipes.json')['recipes']
    by_id = {d['id']: d for d in topics}
    prefix = 'skills/houdini-agent/'
    out = {}
    for d in topics:
        parent = str(PurePosixPath(d['path']).parent)
        cli = os.path.relpath(by_id['cli-contract']['path'], parent).replace(os.sep, '/')
        acceptance = os.path.relpath(by_id['acceptance']['path'], parent).replace(os.sep, '/')
        out[prefix + d['path']] = render_topic(d, sources, registry['reviewed_on'], cli, acceptance)
    for d in recipes:
        out[prefix + d['path']] = render_recipe(d, by_id, sources)
    lines = ['# Houdini Agent Wiki', '',
             f"{len(topics)} 个领域入口 · {len(recipes)} 个任务配方 · {len(sources)} 条来源 · {registry['reviewed_on']}", '',
             '先读 [快速上手](quickstart.md)、[CLI 契约](02-cli-contract.md) 和 [已核对工具候选](tool-map.md)。这里只按需阅读，不要求 Agent 预载全库。', '',
             '## 覆盖等级', '`guide`：原理、输入、操作策略与验收；`discovery`：复杂/新领域的路由与继续阅读入口；`recipe-design-not-runtime-tested`：有任务步骤，尚无目标 Houdini 运行证据。示例通过离线检查不等于效果运行通过。', '',
             '## 领域目录', '| 领域 | Skill | 等级 |', '| --- | --- | --- |']
    for d in topics:
        lines.append(f"| [{d['title']}]({PurePosixPath(d['path']).name}) | `{d['skill']}` | {d['coverage']} |")
    lines += ['', '## 具体任务配方', '每个配方说明最小网络意图、需要现场查询的参数、执行和验收；不是硬编码的可执行节点清单。', '']
    lines += [f"- [{d['title']}]({os.path.relpath(d['path'], 'wiki').replace(os.sep, '/')})" for d in recipes]
    lines += ['', '## 其他入口', '[源码示例与前提](../examples/README.md) · [现场测试矩阵](target-smoke.md) · [来源目录](sources.md) · [验收模板](../templates/acceptance.json)']
    out[prefix + 'wiki/README.md'] = '\n'.join(lines) + '\n'
    lines = ['# 来源与核对深度', '',
             f"整理日期：{registry['reviewed_on']}。共 {len(sources)} 条来源；阅读深度逐条标明，不表示整站、整段视频或全部示例已复现。", '',
             'Git 引用固定 commit；官方和社区网页为滚动地址，没有保存网页快照，`content_sha256: null`。部分社区内容仅核对公开落地页，不包含付费正文、视频或 HIP 文件。', '',
             f"官方在线文档观察值：{registry['houdini_docs_observed']}。CLI 基线与范围见 [现场测试矩阵](target-smoke.md)。", '']
    for s in sources.values():
        lines += [f"## {s['id']} · {s['title']}", f"[原始来源]({s['url']})", '',
                  f"类型: `{s['kind']}` · 核对深度: `{s['review_depth']}` · 核对日期: {s['reviewed_on']} · 固定方式: `{s['pin_kind']}`"]
        if s.get('commit'):
            lines += [f"Commit: `{s['commit']}`"]
        if s.get('note'):
            lines += [s['note']]
        lines.append('')
    out[prefix + 'wiki/sources.md'] = '\n'.join(lines) + '\n'
    return out


def rebuild(root: Path, check=False) -> dict:
    root = root.resolve(strict=True)
    contents = generated_files(root)
    changed = []
    # Resolve the whole plan before writing.
    plan = [(safe_destination(root, path), text) for path, text in contents.items()]
    for path, text in plan:
        if path.is_file() and path.read_text(encoding='utf-8') == text:
            continue
        changed.append(str(path.relative_to(root)).replace(os.sep, '/'))
        if check:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_destination(root, str(path.relative_to(root)).replace(os.sep, '/'))
        fd, tmp = tempfile.mkstemp(prefix='.' + path.name, suffix='.tmp', dir=path.parent)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
                f.write(text)
            os.replace(tmp, path)
        finally:
            Path(tmp).unlink(missing_ok=True)
    return {'ok': not changed if check else True, 'check_only': check, 'generated_pages': len(plan), 'changed': changed}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--check', action='store_true', help='No writes; exit 1 when generated pages differ.')
    a = p.parse_args(argv)
    try:
        result = rebuild(a.root, a.check)
    except (OSError, ValueError, KeyError, TypeError) as e:
        result = {'ok': False, 'error': str(e)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
