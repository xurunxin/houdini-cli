import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { listWiki, searchWiki, readSkill } from '../src/knowledge.mjs';

const cli = fileURLToPath(new URL('../src/cli.mjs', import.meta.url));
function run(...args) {
  const result = spawnSync(process.execPath, [cli, ...args], { cwd: tmpdir(), encoding: 'utf8' });
  return { status: result.status, data: JSON.parse(result.stdout) };
}

test('knowledge commands work outside checkout without setup or MCP', () => {
  const listed = run('skills', 'list');
  assert.equal(listed.status, 0);
  assert.ok(listed.data.skills.some(skill => skill.name === 'houdini-vellum'));
  assert.match(run('skills', 'read', 'houdini-agent').data.skill.content, /Houdini/);
  const searched = run('wiki', 'search', '穿透', '--limit', '2');
  assert.equal(searched.status, 0);
  assert.ok(searched.data.results.length > 0 && searched.data.results.length <= 2);
  assert.match(run('wiki', 'read', searched.data.results[0].id).data.page.content, /穿透/);
  assert.match(run('skills', 'read', 'houdini-agent', 'examples/hom/runtime_probe.py').data.skill.content, /hou/);
});

test('knowledge CLI reports invalid input and missing pages as JSON failures', () => {
  for (const args of [['wiki', 'search', 'vellum', '--limit', '0'], ['wiki', 'read', '../LICENSE'], ['skills', 'read', 'missing']]) {
    const result = run(...args);
    assert.notEqual(result.status, 0);
    assert.equal(result.data.ok, false);
    assert.ok(result.data.error.code);
  }
});

test('catalog includes recipes and search handles English, Chinese and no matches', async () => {
  assert.ok((await listWiki()).some(page => page.id === 'recipes/cloth-penetration'));
  assert.ok((await searchWiki('vElLuM')).length > 0);
  assert.ok((await searchWiki('穿透')).length > 0);
  assert.deepEqual(await searchWiki('unfindable-xyz-927381'), []);
  await assert.rejects(searchWiki(' '), { code: 'INVALID_QUERY' });
  await assert.rejects(readSkill('houdini-agent', '../houdini-vellum/SKILL.md'), { code: 'INVALID_RESOURCE' });
  await assert.rejects(readSkill('houdini-agent', 'C:/Windows/win.ini'), { code: 'INVALID_RESOURCE' });
});
