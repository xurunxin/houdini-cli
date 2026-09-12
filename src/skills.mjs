import { readFile, mkdir, lstat, realpath, writeFile, rename } from 'node:fs/promises';
import { dirname, join, resolve, relative, sep } from 'node:path';
import { randomUUID } from 'node:crypto';
import { ensure } from './core.mjs';
import { readSkill } from './knowledge.mjs';

async function checkParents(root, destination) {
  const path = relative(root, destination);
  ensure(path && path !== '..' && !path.startsWith(`..${sep}`), 'INVALID_TARGET', 'Skill 必须位于目标项目内。');
  let current = root;
  for (const part of path.split(sep)) {
    current = join(current, part);
    try { ensure(!(await lstat(current)).isSymbolicLink(), 'UNSAFE_TARGET', 'Skill 目标包含符号链接或 junction。'); }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
  }
}
export async function installSkills(metadata, options = {}) {
  const agent = options.agent || 'codex';
  ensure(['codex', 'claude', 'all'].includes(agent), 'INVALID_AGENT', '--agent 可选 codex、claude、all。');
  const root = await realpath(resolve(options.target || process.cwd()));
  ensure((await lstat(root)).isDirectory(), 'INVALID_TARGET', '--target 必须是已有项目目录。');
  const selected = options.name || metadata.id;
  const names = selected === metadata.id ? [selected] : selected === 'houdini-agent' ? [metadata.id, selected] : [metadata.id, 'houdini-agent', selected];
  const files = [];
  for (const name of names) {
    const skill = await readSkill(name);
    for (const resource of new Set(['SKILL.md', ...skill.resources])) {
      files.push({ name, resource, content: resource === 'SKILL.md' ? skill.content : (await readSkill(name, resource)).content });
    }
  }
  const directories = agent === 'all' ? ['.agents', '.claude'] : [agent === 'codex' ? '.agents' : '.claude'];
  const planned = [];
  for (const directory of directories) {
    for (const { name, resource, content } of files) {
      const path = join(root, directory, 'skills', name, resource);
      await checkParents(root, path);
      let existing = null;
      try { existing = await readFile(path, 'utf8'); } catch (e) { if (e.code !== 'ENOENT') throw e; }
      ensure(existing === null || existing === content || options.force, 'SKILL_CONFLICT', `已有定制 skill：${path}。检查后可用 --force 更新。`);
      planned.push({ path, content, status: existing === content ? 'unchanged' : existing === null ? 'installed' : 'updated' });
    }
  }
  if (!options.dryRun) for (const item of planned) {
    if (item.status === 'unchanged') continue;
    await checkParents(root, item.path);
    await mkdir(dirname(item.path), { recursive: true });
    if (item.status === 'installed') await writeFile(item.path, item.content, { flag: 'wx' });
    else {
      const temp = `${item.path}.${randomUUID()}.tmp`;
      await writeFile(temp, item.content, { flag: 'wx' });
      await rename(temp, item.path);
    }
  }
  return { project: root, agent, dryRun: !!options.dryRun, skills: planned.map(({ content, ...item }) => item) };
}
