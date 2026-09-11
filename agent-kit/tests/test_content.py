from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value
R = module('rebuild_wiki', ROOT/'tools/rebuild_wiki.py')
S = module('build_site', ROOT/'tools/build_site.py')
I = module('install_kit', ROOT/'tools/install_kit.py')

class ContentTests(unittest.TestCase):
    def test_generated_content_synchronized(self):
        self.assertTrue(R.rebuild(ROOT, check=True)['ok'])
    def test_generated_page_count(self):
        self.assertEqual(len(R.generated_files(ROOT)), 74)
    def test_rebuild_refuses_escape(self):
        with self.assertRaises(ValueError):
            R.safe_destination(ROOT, '../outside.md')
    def test_renderer_escapes_html(self):
        result = S.render_markdown('<script>alert(1)</script>', 'README.md', {'README.md'})
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;script&gt;', result)
    def test_renderer_rejects_javascript_links(self):
        self.assertNotIn('href=', S.inline('[x](javascript:bad)', 'README.md', {'README.md'}))
    def test_relative_link_resolution(self):
        self.assertEqual(S.local_target('a/b/x.md', '../y.md'), 'a/y.md')
        self.assertIn('#doc=a/y.md', S.inline('[y](../y.md)', 'a/b/x.md', {'a/y.md'}))
    def test_core_install_runs_real_query(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            report = I.install(ROOT, target)
            self.assertTrue(report['ok'])
            tool = target/'.agents/skills/houdini-agent/tools/query.py'
            result = subprocess.run([sys.executable, str(tool), 'search', '布料穿透', '--limit', '1'], capture_output=True, text=True, encoding='utf-8', check=True)
            hit = json.loads(result.stdout)['results'][0]
            self.assertEqual(hit['skill'], 'houdini-vellum')
            self.assertTrue((tool.parent.parent/hit['path']).is_file())
    def test_all_real_skills_install(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            I.install(ROOT, target, agent='all', profile='all')
            for agent in ('.agents', '.claude'):
                self.assertEqual(len(list((target/agent/'skills').glob('*/SKILL.md'))), 20)
    def test_embedded_skill_count(self):
        self.assertEqual(sum(d['kind']=='skill' for d in S.collect(ROOT)), 20)
    def test_no_control_characters_in_markdown(self):
        for p in ROOT.rglob('*.md'):
            self.assertFalse(any(b < 32 and b != 10 for b in p.read_bytes()), str(p))

if __name__ == '__main__':
    unittest.main()
