# Agent instructions for maintaining this kit

Use `skills/houdini-agent/SKILL.md` as the execution router. Knowledge lives in the self-contained hub, not in external absolute paths.

Do not modify the upstream houdini-cli implementation or its existing skill merely to install this pack. It is an additive package. Do not start Houdini for documentation-only tasks.

Knowledge records in `index/topics.json` and `index/recipes.json` must stay synchronized with their Wiki pages. Use `tools/rebuild_wiki.py` and `tools/build_site.py` after editing records, then run the validator/tests. Source records must identify exact links, review depth, date, and runtime validation scope. A rolling URL with a null content hash is NOT a pinned document snapshot.

Test commands (from this directory):

```bash
python tools/validate_kit.py .
python -m unittest discover -s tests -v
```

No `hou` runtime is assumed in the ordinary test suite. Static Python tests do not validate Houdini operators, VEX compilation, simulation results or renders. Never mark runtime-tested without a target build, procedure and evidence.

Preserve unknown user files, reject path escapes, keep CLI calls serial, and do not replay timed-out mutations. New effects start as design recipes; promote only after reproducible target-Houdini evidence exists.
