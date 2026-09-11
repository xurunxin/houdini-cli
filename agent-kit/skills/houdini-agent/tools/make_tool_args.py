#!/usr/bin/env python3
"""Package reviewed Python using a saved live tools-inspect schema. NEVER execute it.

The local script is embedded as source text, not as a path on the Houdini host.
Requires an explicit string property name; does not guess the tool's code key.
JSON Schema constraints are checked by jsonschema when installed. Otherwise only
required/properties/basic types/enum/additionalProperties are checked and reported.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

def object_file(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(obj, dict):
        raise ValueError(f'{path}: expected a JSON object')
    return obj

def extract_tool(snapshot: dict) -> dict:
    if snapshot.get('ok') is False:
        raise ValueError('tools inspect snapshot reports failure')
    tool = snapshot.get('tool', snapshot)
    if not isinstance(tool, dict) or not isinstance(tool.get('name'), str):
        raise ValueError('expected {tool:{name,inputSchema}} or a tool object')
    schema = tool.get('inputSchema')
    if not isinstance(schema, dict) or schema.get('type') != 'object':
        raise ValueError('expected an object inputSchema from tools inspect')
    return tool

def basic_validate(value: dict, schema: dict) -> None:
    props = schema.get('properties', {})
    for key in schema.get('required', []):
        if key not in value:
            raise ValueError(f'missing required tool property: {key}')
    if schema.get('additionalProperties') is False:
        unknown = set(value) - set(props)
        if unknown:
            raise ValueError(f'unknown tool properties: {sorted(unknown)}')
    for key, val in value.items():
        spec = props.get(key, {})
        t = spec.get('type')
        checks = {'string': lambda: isinstance(val, str),
                  'integer': lambda: isinstance(val, int) and not isinstance(val, bool),
                  'number': lambda: isinstance(val, (int, float)) and not isinstance(val, bool),
                  'boolean': lambda: isinstance(val, bool), 'object': lambda: isinstance(val, dict),
                  'array': lambda: isinstance(val, list), 'null': lambda: val is None}
        if isinstance(t, str) and t in checks and not checks[t]():
            raise ValueError(f'{key}: expected {t}')
        if 'enum' in spec and val not in spec['enum']:
            raise ValueError(f'{key}: not in enum')

def build_args(snapshot: dict, source: str, code_field: str, config: dict | None = None,
               extra: dict | None = None) -> tuple[str, dict, str]:
    tool = extract_tool(snapshot); schema = tool['inputSchema']
    spec = schema.get('properties', {}).get(code_field)
    if not isinstance(spec, dict) or spec.get('type') != 'string':
        raise ValueError(f'{code_field!r} must be an explicit string property in the live schema; inspect unions/refs manually')
    if (config is not None and not isinstance(config, dict)) or (extra is not None and not isinstance(extra, dict)):
        raise ValueError('config and extra must be JSON objects')
    compile(source, '<reviewed-houdini-agent-script>', 'exec')  # syntax only
    args = dict(extra or {})
    if code_field in args:
        raise ValueError('extra must not override the code property')
    config_json = json.dumps(config or {}, ensure_ascii=False, allow_nan=False)
    # Separate globals/locals supported by upstream; source executes in one isolated namespace.
    wrapped = ('import json as _ha_json\n'
               '_ha_scope = {"__name__": "__main__", "HOUDINI_AGENT_CONFIG": '
               f'_ha_json.loads({config_json!r})' + '}\n'
               f'exec(compile({source!r}, "<houdini-agent-script>", "exec"), _ha_scope, _ha_scope)\n')
    args[code_field] = wrapped
    basic_validate(args, schema)
    validation = 'basic-subset-only; not full JSON Schema validation'
    try:
        import jsonschema
    except ImportError:
        pass
    else:
        validator_class = jsonschema.validators.validator_for(schema)
        validator_class.check_schema(schema)
        # No remote references allowed; avoids network fetching during local validation.
        def remote_refs(obj):
            if isinstance(obj, dict):
                for k,v in obj.items():
                    if k == '$ref' and isinstance(v,str) and not v.startswith('#'):
                        raise ValueError('external schema references are not resolved; inspect schema manually')
                    remote_refs(v)
            elif isinstance(obj, list):
                for v in obj: remote_refs(v)
        remote_refs(schema)
        validator_class(schema).validate(args)
        validation = 'jsonschema (local schema only)'
    return tool['name'], args, validation

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--schema', required=True, type=Path); p.add_argument('--script', required=True, type=Path)
    p.add_argument('--code-field', required=True); p.add_argument('--config', type=Path); p.add_argument('--extra', type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args(argv)
    try:
        tool, args, validation = build_args(object_file(a.schema), a.script.read_text(encoding='utf-8-sig'),
                                            a.code_field, object_file(a.config) if a.config else {},
                                            object_file(a.extra) if a.extra else {})
        # Exclusive create: never overwrite a previous, potentially still-running request.
        with a.output.open('x', encoding='utf-8', newline='\n') as out:
            json.dump(args, out, ensure_ascii=False, indent=2, allow_nan=False); out.write('\n')
        print(json.dumps({'ok': True, 'tool': tool, 'output': str(a.output.resolve()),
                          'validation': validation, 'executed': False,
                          'next': 'review the args, then use houdini-cli --session TASK tools call ACTUAL_TOOL --args-file OUTPUT'}, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({'ok': False, 'error': str(e), 'executed': False}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
