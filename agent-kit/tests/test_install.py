from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('install',ROOT/'tools/install_kit.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.source=self.base/'source';self.target=self.base/'project';self.target.mkdir()
        for skill in ['houdini-agent','houdini-sop']:
            p=self.source/'skills'/skill/'SKILL.md';p.parent.mkdir(parents=True);p.write_text('test skill '+skill)
        p=self.source/'skills/houdini-agent/wiki/test.md';p.parent.mkdir();p.write_text('knowledge')
    def tearDown(self):self.tmp.cleanup()
    def test_dry_run_no_write(self):
        r=M.install(self.source,self.target,dry_run=True);self.assertTrue(r['ok']);self.assertFalse((self.target/'.agents').exists())
    def test_core_recursive(self):
        M.install(self.source,self.target);self.assertTrue((self.target/'.agents/skills/houdini-agent/wiki/test.md').is_file());self.assertFalse((self.target/'.agents/skills/houdini-sop').exists())
    def test_all_agents_and_skills(self):
        M.install(self.source,self.target,agent='all',profile='all')
        for agent in ['.agents','.claude']:self.assertTrue((self.target/agent/'skills/houdini-sop/SKILL.md').is_file())
    def test_idempotent(self):
        M.install(self.source,self.target);r=M.install(self.source,self.target);self.assertEqual(r['counts']['install'],0);self.assertEqual(r['counts']['update'],0)
    def test_custom_conflict_no_partial_write(self):
        p=self.target/'.agents/skills/houdini-agent/wiki/test.md';p.parent.mkdir(parents=True);p.write_text('custom')
        with self.assertRaises(ValueError):M.install(self.source,self.target)
        self.assertFalse((self.target/'.agents/skills/houdini-agent/SKILL.md').exists());self.assertEqual(p.read_text(),'custom')
    def test_force_backup(self):
        M.install(self.source,self.target);p=self.target/'.agents/skills/houdini-agent/wiki/test.md';p.write_text('custom')
        r=M.install(self.source,self.target,force=True);self.assertIsNotNone(r['backup']);backup=Path(r['backup'])/'.agents/skills/houdini-agent/wiki/test.md'
        self.assertEqual(backup.read_text(),'custom');self.assertEqual(p.read_text(),'knowledge')
    def test_preserve_original_cli_and_unknown(self):
        for path in ['.agents/skills/houdini-cli/SKILL.md','.agents/skills/houdini-agent/custom.txt']:
            p=self.target/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('keep')
        M.install(self.source,self.target)
        self.assertEqual((self.target/'.agents/skills/houdini-cli/SKILL.md').read_text(),'keep')
        self.assertEqual((self.target/'.agents/skills/houdini-agent/custom.txt').read_text(),'keep')
    def test_symlink_parent_rejected(self):
        other=self.base/'outside';other.mkdir()
        try:(self.target/'.agents').symlink_to(other,target_is_directory=True)
        except OSError:self.skipTest('symlink unavailable')
        with self.assertRaises(ValueError):M.install(self.source,self.target,force=True)
        self.assertEqual(list(other.iterdir()),[])
    def test_source_symlink_rejected(self):
        target=self.source/'skills/houdini-agent/wiki/link.txt'
        try:target.symlink_to(self.source/'skills/houdini-sop/SKILL.md')
        except OSError:self.skipTest('symlink unavailable')
        with self.assertRaises(ValueError):M.install(self.source,self.target)
    def test_invalid_agent(self):
        with self.assertRaises(ValueError):M.install(self.source,self.target,agent='bad')
    def test_missing_target(self):
        with self.assertRaises(OSError):M.install(self.source,self.target/'missing')
if __name__=='__main__':unittest.main()
