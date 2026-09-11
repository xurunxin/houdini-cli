# Maintaining the Houdini agent kit

Open files relevant to the change. Use `skills/houdini-agent/SKILL.md` for unclear or cross-domain tasks; start a known specialty directly. Documentation work does not launch Houdini.

Keep knowledge self-contained in `skills/houdini-agent`, links relative and installation recursive. Installing this kit does not require changing the CLI.

For knowledge edits, update `skills/houdini-agent/index/topics.json` or `recipes.json`, then run `python tools/rebuild_wiki.py`. Changed embedded documents require `python tools/build_site.py`; refresh `MANIFEST.sha256` last. Consult `CONTRIBUTING.md` for source or packaging changes.

From this directory, `python tools/validate_kit.py .` checks structure/links; `python -m unittest discover -s tests -v` uses offline fixtures, no production or `hou`. Run relevant checks and fix caused failures without reconfirming authorized reversible work; finish with evidence or a concrete blocker.

Preserve unknown files and path-escape protections. Bridge calls stay serial; never replay unknown timed-out mutations. Source records need exact links, review depth, date and runtime scope; null hashes do not pin rolling URLs. Recipes remain design-only until target-build evidence exists. Offline tests do not validate Houdini operators, VEX, simulations or renders.
