import { readdir, readFile, realpath } from 'node:fs/promises';
import { resolve, relative, sep, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ensure } from './core.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const kit = resolve(root, 'agent-kit/skills');
const wiki = resolve(kit, 'houdini-agent/wiki');

function validPath(value) {
  return typeof value === 'string' && value.length > 0 && !value.includes('\\') &&
    value.split('/').every(part => part && part !== '.' && part !== '..' && !/[:\x00-\x1f]/.test(part));
}
async function safeFile(base, name, code) {
  ensure(validPath(name), 'INVALID_RESOURCE', '请使用目录内的相对路径。');
  const path = resolve(base, name);
  let actual;
  try { actual = await realpath(path); }
  catch (error) { if (error.code !== 'ENOENT' && error.code !== 'ENOTDIR') throw error; ensure(false, code, `资源不存在：${name}`); }
  const rel = relative(await realpath(base), actual);
  ensure(rel && !isAbsolute(rel) && rel !== '..' && !rel.startsWith(`..${sep}`), 'INVALID_RESOURCE', '资源必须位于技能目录内。');
  return actual;
}
async function files(base, prefix = '') {
  const result = [];
  for (const entry of await readdir(resolve(base, prefix), { withFileTypes: true })) {
    const name = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) result.push(...await files(base, name));
    else if (entry.isFile()) result.push(name);
  }
  return result.sort();
}
async function skillRoot(name) {
  ensure(typeof name === 'string' && /^[a-z0-9-]+$/.test(name), 'INVALID_SKILL', '技能名称必须来自 skills list。');
  const base = name === 'houdini-cli' ? resolve(root, 'skills') : kit;
  return safeFile(base, name, 'UNKNOWN_SKILL');
}
function title(content, fallback) { return content.match(/^#\s+(.+)$/m)?.[1].trim() || fallback; }

export async function listSkills() {
  const names = ['houdini-cli', ...(await readdir(kit, { withFileTypes: true })).filter(e => e.isDirectory()).map(e => e.name)].sort();
  return Promise.all(names.map(async name => {
    const base = await skillRoot(name);
    const content = await readFile(await safeFile(base, 'SKILL.md', 'UNKNOWN_SKILL'), 'utf8');
    return { name, description: content.match(/^description:\s*(.+)$/m)?.[1].trim() || '' };
  }));
}
export async function readSkill(name, resource = 'SKILL.md') {
  const base = await skillRoot(name);
  const path = await safeFile(base, resource, 'UNKNOWN_RESOURCE');
  const content = await readFile(path, 'utf8');
  return { name, resource, path, content, resources: resource === 'SKILL.md' ? await files(base) : [] };
}
export async function listWiki() {
  const pages = (await files(wiki)).filter(path => path.endsWith('.md'));
  return Promise.all(pages.map(async path => {
    const id = path.slice(0, -3);
    return { id, title: title(await readFile(await safeFile(wiki, path, 'UNKNOWN_PAGE'), 'utf8'), id), path };
  }));
}
export async function readWiki(id) {
  ensure(validPath(id), 'INVALID_PAGE', '页面 id 必须来自 wiki list/search。');
  const normalized = id.endsWith('.md') ? id.slice(0, -3) : id;
  const path = `${normalized}.md`;
  const content = await readFile(await safeFile(wiki, path, 'UNKNOWN_PAGE'), 'utf8');
  return { id: normalized, title: title(content, normalized), path, content };
}
export async function searchWiki(query, { limit = 10 } = {}) {
  ensure(typeof query === 'string' && query.trim(), 'INVALID_QUERY', '查询不能为空。');
  ensure(Number.isSafeInteger(limit) && limit > 0 && limit <= 2147483647, 'INVALID_LIMIT', 'limit 必须是正整数。');
  const term = query.trim().toLowerCase();
  const matches = [];
  for (const page of await listWiki()) {
    const { content } = await readWiki(page.id);
    const position = content.toLowerCase().indexOf(term);
    const headingMatch = `${page.id} ${page.title}`.toLowerCase().includes(term);
    if (position < 0 && !headingMatch) continue;
    matches.push({ ...page, snippet: content.slice(Math.max(0, position - 100), Math.max(0, position - 100) + 400), score: headingMatch ? 1 : 0 });
  }
  return matches.sort((a, b) => b.score - a.score || a.id.localeCompare(b.id)).slice(0, limit).map(({ score, ...page }) => page);
}
