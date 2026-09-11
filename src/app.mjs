import { execFileSync, spawn as spawnProcess } from 'node:child_process';
import { closeSync, existsSync, mkdirSync, openSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import net from 'node:net';
import { delimiter, dirname, isAbsolute, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const metadata = {
  id: 'houdini-cli',
  bin: 'houdini-cli',
  label: 'Houdini',
  defaultPort: 9877,
  mcpNames: ['houdini-mcp', 'houdini'],
};

const UPSTREAM_URL = 'https://github.com/capoomgit/houdini-mcp.git';
const UPSTREAM_REVISION = 'de4fd93acc207fc57c02b330d421461f5963a945';
const DEFAULT_APP_PATH = 'C:\\Program Files\\Side Effects Software\\Houdini 22.0.368\\bin\\houdini.exe';
const ASSET_DIR = fileURLToPath(new URL('../assets/', import.meta.url));
const PYTHON_VERSIONS = ['3.9', '3.10', '3.11', '3.12', '3.13'];
const SOURCE_FILES = ['__init__.py', 'server.py', 'HoudiniMCPRender.py', 'houdini_mcp_server.py'];

function codedError(message, code) {
  return Object.assign(new Error(message), { code });
}

function asAbsolute(value, name, base = process.cwd()) {
  if (!value || typeof value !== 'string') {
    throw codedError(`${name} is required.`, 'CONFIG_REQUIRED');
  }
  return isAbsolute(value) ? resolve(value) : resolve(base, value);
}

function normalizePort(value) {
  const port = Number(value ?? metadata.defaultPort);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw codedError(`Invalid port: ${value}`, 'INVALID_PORT');
  }
  return port;
}

function normalizeHost(value) {
  const host = String(value ?? '127.0.0.1').trim().toLowerCase();
  if (!['127.0.0.1', 'localhost', '::1'].includes(host)) {
    throw codedError('Houdini MCP may only listen on the local loopback interface.', 'HOST_NOT_LOOPBACK');
  }
  // The upstream stdio bridge currently connects to 127.0.0.1 internally.
  return '127.0.0.1';
}

function versionParts(name) {
  const match = /^Houdini\s+(\d+(?:\.\d+)+)$/i.exec(name);
  return match ? match[1].split('.').map(Number) : null;
}

function compareVersionsDescending(left, right) {
  const length = Math.max(left.version.length, right.version.length);
  for (let index = 0; index < length; index += 1) {
    const difference = (right.version[index] ?? 0) - (left.version[index] ?? 0);
    if (difference) return difference;
  }
  return 0;
}

function discoverHoudiniApp(exec) {
  const candidates = [];
  const programRoots = [...new Set([process.env.ProgramFiles, process.env['ProgramFiles(x86)']].filter(Boolean))];
  for (const programRoot of programRoots) {
    const sidefxRoot = join(programRoot, 'Side Effects Software');
    try {
      for (const entry of readdirSync(sidefxRoot, { withFileTypes: true })) {
        if (!entry.isDirectory()) continue;
        const version = versionParts(entry.name);
        if (!version) continue;
        const candidate = join(sidefxRoot, entry.name, 'bin', process.platform === 'win32' ? 'houdini.exe' : 'houdini');
        if (existsSync(candidate)) candidates.push({ candidate, version });
      }
    } catch {
      // This Program Files root is absent or unreadable.
    }
  }
  candidates.sort(compareVersionsDescending);
  if (candidates.length) return candidates[0].candidate;
  return discoverExecutable(process.platform === 'win32' ? 'houdini.exe' : 'houdini', exec) ?? DEFAULT_APP_PATH;
}

function mergedConfig(config = {}, options = {}) {
  const stateDir = asAbsolute(config.stateDir, 'stateDir');
  const exec = options.execFileSync ?? execFileSync;
  return {
    ...config,
    stateDir,
    appPath: asAbsolute(options.appPath ?? config.appPath ?? discoverHoudiniApp(exec), 'appPath'),
    uvPath: options.uvPath ?? config.uvPath ?? 'uv',
    host: normalizeHost(options.host ?? config.host),
    port: normalizePort(options.port ?? config.port),
    ...(options.source !== undefined ? { source: asAbsolute(options.source, 'source') } : {}),
    ...(options.serverPath !== undefined ? { serverPath: asAbsolute(options.serverPath, 'serverPath') } : {}),
  };
}

function pathsFor(config) {
  const runtimeDir = config.runtimePath ?? join(config.stateDir, 'runtime');
  const pluginPath = config.pluginPath ?? join(config.stateDir, 'houdini-path');
  return {
    runtimeDir,
    pluginPath,
    bridgePath: config.bridgePath ?? join(runtimeDir, 'houdini_mcp_server.py'),
    pythonPath: config.pythonPath ?? join(runtimeDir, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python'),
    manifestPath: join(config.stateDir, 'setup-manifest.json'),
    headlessRunner: join(pluginPath, 'headless_runner.py'),
  };
}

function sourceProblems(source) {
  return SOURCE_FILES.filter((name) => !existsSync(join(source, name)));
}

function readAsset(name) {
  return readFileSync(join(ASSET_DIR, name), 'utf8');
}

function prepareBridge(sourceText) {
  if (sourceText.includes('from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser')) {
    return { text: sourceText, patches: [] };
  }

  const legacyImport = /^([ \t]*)from langchain\.output_parsers import ResponseSchema, StructuredOutputParser\s*$/m;
  if (legacyImport.test(sourceText)) {
    const text = sourceText.replace(
      legacyImport,
      '$1try:\n$1    from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser\n$1except ImportError:\n$1    from langchain.output_parsers import ResponseSchema, StructuredOutputParser',
    );
    return { text, patches: ['prefer-langchain-classic-output-parsers'] };
  }

  if (/\b(ResponseSchema|StructuredOutputParser)\b/.test(sourceText)) {
    const insertion = [
      'try:',
      '    from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser',
      'except ImportError:',
      '    from langchain.output_parsers import ResponseSchema, StructuredOutputParser',
      '',
    ].join('\n');
    return {
      text: sourceText.replace(/^(import sys\s*)$/m, `$1\n${insertion}`),
      patches: ['add-langchain-output-parser-import'],
    };
  }

  return { text: sourceText, patches: [] };
}

function run(exec, command, args, options = {}) {
  try {
    return exec(command, args, {
      encoding: 'utf8',
      shell: false,
      windowsHide: true,
      stdio: ['ignore', 'pipe', 'pipe'],
      ...options,
    });
  } catch (error) {
    const detail = String(error.stderr || error.stdout || error.message || error).trim();
    throw codedError(`${command} ${args.join(' ')} failed${detail ? `: ${detail}` : ''}`, 'SUBPROCESS_FAILED');
  }
}

function discoverExecutable(value, exec = execFileSync) {
  if (isAbsolute(value)) return existsSync(value) ? value : null;
  const locator = process.platform === 'win32' ? 'where.exe' : 'which';
  try {
    const result = exec(locator, [value], {
      encoding: 'utf8',
      shell: false,
      windowsHide: true,
      stdio: ['ignore', 'pipe', 'ignore'],
    });
    return String(result).split(/\r?\n/).map((line) => line.trim()).find(Boolean) ?? null;
  } catch {
    return null;
  }
}

function gitInfo(source, exec) {
  if (!existsSync(join(source, '.git'))) return { revision: null, dirty: null };
  try {
    const revision = String(run(exec, 'git', ['-C', source, 'rev-parse', 'HEAD'])).trim();
    const dirty = String(run(exec, 'git', ['-C', source, 'status', '--porcelain'])).trim().length > 0;
    return { revision, dirty };
  } catch {
    return { revision: null, dirty: null };
  }
}

function clonePinnedSource(destination, exec, timeout) {
  mkdirSync(dirname(destination), { recursive: true });
  run(exec, 'git', ['init', destination], { timeout });
  run(exec, 'git', ['-C', destination, 'remote', 'add', 'origin', UPSTREAM_URL], { timeout });
  run(exec, 'git', ['-C', destination, 'fetch', '--depth', '1', 'origin', UPSTREAM_REVISION], { timeout });
  run(exec, 'git', ['-C', destination, 'checkout', '--detach', 'FETCH_HEAD'], { timeout });
  const revision = String(run(exec, 'git', ['-C', destination, 'rev-parse', 'HEAD'])).trim();
  if (revision !== UPSTREAM_REVISION) {
    throw codedError(`Downloaded Houdini MCP revision ${revision}, expected ${UPSTREAM_REVISION}.`, 'SOURCE_VERSION_MISMATCH');
  }
}

function writeOwnedAssets(config, source, bridge, patches) {
  const paths = pathsFor(config);
  mkdirSync(paths.runtimeDir, { recursive: true });
  mkdirSync(paths.pluginPath, { recursive: true });

  writeFileSync(join(paths.runtimeDir, 'pyproject.toml'), readAsset('runtime-pyproject.toml'), 'utf8');
  writeFileSync(paths.bridgePath, bridge, 'utf8');
  writeFileSync(paths.headlessRunner, readAsset('headless_runner.py'), 'utf8');
  for (const version of PYTHON_VERSIONS) {
    const startupDir = join(paths.pluginPath, `python${version}libs`);
    mkdirSync(startupDir, { recursive: true });
    writeFileSync(join(startupDir, 'ready.py'), readAsset('ready.py'), 'utf8');
  }

  const manifest = {
    schemaVersion: 1,
    source,
    sourceServerPath: config.serverPath,
    bridgePath: paths.bridgePath,
    upstream: { url: UPSTREAM_URL, revision: UPSTREAM_REVISION },
    patches,
  };
  writeFileSync(paths.manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  return paths;
}

export async function setup(config, options = {}) {
  const merged = mergedConfig(config, options);
  const exec = options.execFileSync ?? execFileSync;
  const timeout = Number(options.timeout ?? 180_000);
  const defaultSource = join(merged.stateDir, 'sources', 'houdinimcp');
  const source = asAbsolute(options.source ?? merged.source ?? defaultSource, 'source');
  const sourceOwned = source === resolve(defaultSource)
    && (config.sourceOwned === true || (options.source === undefined && config.source === undefined));
  const sourceServerPath = asAbsolute(options.serverPath ?? merged.serverPath ?? join(source, 'houdini_mcp_server.py'), 'serverPath');
  const desired = {
    ...merged,
    source,
    serverPath: sourceServerPath,
    runtimePath: join(merged.stateDir, 'runtime'),
    pluginPath: join(merged.stateDir, 'houdini-path'),
    bridgePath: join(merged.stateDir, 'runtime', 'houdini_mcp_server.py'),
    pythonPath: join(merged.stateDir, 'runtime', '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python'),
    sourceOwned,
    upstreamRevision: sourceOwned ? UPSTREAM_REVISION : undefined,
  };

  const plan = [
    ...(existsSync(source) ? [] : [`download ${UPSTREAM_URL}@${UPSTREAM_REVISION} to ${source}`]),
    `write isolated Python runtime to ${desired.runtimePath}`,
    `write process-scoped Houdini startup hooks to ${desired.pluginPath}`,
    `sync pinned dependencies with ${desired.uvPath}`,
  ];
  if (options.dryRun) return { config: desired, dryRun: true, plan };

  mkdirSync(merged.stateDir, { recursive: true });
  if (!existsSync(source)) {
    if (!sourceOwned) throw codedError(`Source directory does not exist: ${source}`, 'SOURCE_NOT_FOUND');
    clonePinnedSource(source, exec, timeout);
  }

  const missing = sourceProblems(source);
  if (missing.length) {
    throw codedError(`Invalid Houdini MCP source at ${source}; missing: ${missing.join(', ')}`, 'INVALID_SOURCE');
  }
  if (!existsSync(sourceServerPath)) {
    throw codedError(`Houdini MCP bridge script does not exist: ${sourceServerPath}`, 'SERVER_NOT_FOUND');
  }

  const info = gitInfo(source, exec);
  if (sourceOwned && info.revision && info.revision !== UPSTREAM_REVISION) {
    throw codedError(`Owned source is at ${info.revision}; expected ${UPSTREAM_REVISION}. Choose a new state directory.`, 'SOURCE_VERSION_MISMATCH');
  }

  const prepared = prepareBridge(readFileSync(sourceServerPath, 'utf8'));
  const paths = writeOwnedAssets(desired, source, prepared.text, prepared.patches);
  const uvPath = discoverExecutable(desired.uvPath, exec) ?? desired.uvPath;
  run(exec, uvPath, ['sync', '--project', paths.runtimeDir, '--no-dev'], { timeout });
  if (!existsSync(paths.pythonPath)) {
    throw codedError(`uv did not create the isolated Python executable: ${paths.pythonPath}`, 'PYTHON_NOT_FOUND');
  }
  const importCheck = [
    'import runpy',
    `runpy.run_path(${JSON.stringify(paths.bridgePath)}, run_name='houdini_cli_bootstrap_check')`,
  ].join('; ');
  run(exec, paths.pythonPath, ['-c', importCheck], { timeout });

  return {
    config: { ...desired, uvPath },
    source: { owned: sourceOwned, revision: info.revision, dirty: info.dirty },
    patches: prepared.patches,
    plan,
  };
}

function check(name, ok, detail) {
  return { name, ok: Boolean(ok), detail };
}

export async function doctor(config, options = {}) {
  let merged;
  try {
    merged = mergedConfig(config, options);
  } catch (error) {
    return { ok: false, checks: [check('configuration', false, `${error.code ?? 'ERROR'}: ${error.message}`)] };
  }

  const exec = options.execFileSync ?? execFileSync;
  const paths = pathsFor(merged);
  const source = merged.source ? asAbsolute(merged.source, 'source') : null;
  const checks = [];
  checks.push(check('state directory', existsSync(merged.stateDir), merged.stateDir));
  checks.push(check('loopback endpoint', merged.host === '127.0.0.1', `${merged.host}:${merged.port}`));
  checks.push(check('Houdini application', existsSync(merged.appPath), merged.appPath));
  const uvPath = discoverExecutable(merged.uvPath, exec);
  checks.push(check('uv executable', Boolean(uvPath), uvPath ?? String(merged.uvPath)));

  if (!source) {
    checks.push(check('Houdini MCP source', false, 'Run setup first or configure source.'));
  } else {
    const missing = existsSync(source) ? sourceProblems(source) : SOURCE_FILES;
    const info = existsSync(source) ? gitInfo(source, exec) : { revision: null, dirty: null };
    const detail = missing.length
      ? `${source}; missing ${missing.join(', ')}`
      : `${source}${info.revision ? ` @ ${info.revision}` : ''}${info.dirty ? ' (external working tree is dirty and remains untouched)' : ''}`;
    checks.push(check('Houdini MCP source', missing.length === 0, detail));
  }

  checks.push(check('isolated Python project', existsSync(join(paths.runtimeDir, 'pyproject.toml')), paths.runtimeDir));
  checks.push(check('isolated Python executable', existsSync(paths.pythonPath), paths.pythonPath));
  checks.push(check('generated MCP bridge', existsSync(paths.bridgePath), paths.bridgePath));
  const readyFiles = PYTHON_VERSIONS.map((version) => join(paths.pluginPath, `python${version}libs`, 'ready.py'));
  checks.push(check('owned Houdini startup hook', readyFiles.some(existsSync), paths.pluginPath));

  const hythonPath = join(dirname(merged.appPath), process.platform === 'win32' ? 'hython.exe' : 'hython');
  if (!existsSync(hythonPath)) {
    checks.push(check('Houdini Python and Qt', false, `Missing ${hythonPath}`));
  } else if (options.probeRuntime === false) {
    checks.push(check('Houdini Python and Qt', true, `${hythonPath} (probe skipped)`));
  } else {
    try {
      const probe = String(run(exec, hythonPath, ['-c', 'import sys; from PySide6 import QtCore; print(f"Python {sys.version_info.major}.{sys.version_info.minor}; Qt {QtCore.qVersion()}")'], { timeout: Number(options.timeout ?? 30_000) })).trim();
      checks.push(check('Houdini Python and Qt', true, probe || hythonPath));
    } catch (error) {
      checks.push(check('Houdini Python and Qt', false, error.message));
    }
  }

  return { ok: checks.every((item) => item.ok), checks, config: merged };
}

function houdiniPathWithOwnedStartup(pluginPath, currentValue) {
  const current = String(currentValue ?? '').split(delimiter).map((part) => part.trim()).filter(Boolean);
  const withoutOwnedOrDefault = current.filter((part) => part !== '&' && resolve(part) !== resolve(pluginPath));
  return [pluginPath, ...withoutOwnedOrDefault, '&'].join(delimiter);
}

function canConnect(host, port, timeout = 400) {
  return new Promise((resolveConnection) => {
    const socket = net.createConnection({ host, port });
    const done = (result) => {
      socket.removeAllListeners();
      socket.destroy();
      resolveConnection(result);
    };
    socket.setTimeout(timeout);
    socket.once('connect', () => done(true));
    socket.once('timeout', () => done(false));
    socket.once('error', () => done(false));
  });
}

async function waitForBridge(child, host, port, timeout) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeout) {
    if (await canConnect(host, port, 300)) return;
    if (child.exitCode !== null) {
      throw codedError(`Houdini exited with code ${child.exitCode} before its MCP bridge started.`, 'APP_EXITED');
    }
    await new Promise((resolveWait) => setTimeout(resolveWait, 150));
  }
  throw codedError(`Houdini process ${child.pid} did not open ${host}:${port} within ${timeout} ms.`, 'BRIDGE_TIMEOUT');
}

export async function launch(config, options = {}) {
  const merged = mergedConfig(config, options);
  const paths = pathsFor(merged);
  const source = merged.source ? asAbsolute(merged.source, 'source') : null;
  if (!source || sourceProblems(source).length) {
    throw codedError('Houdini MCP source is not configured. Run setup first.', 'NOT_SETUP');
  }
  if (!existsSync(paths.headlessRunner) || !PYTHON_VERSIONS.some((version) => existsSync(join(paths.pluginPath, `python${version}libs`, 'ready.py')))) {
    throw codedError('Owned Houdini startup files are missing. Run setup first.', 'NOT_SETUP');
  }

  const headless = Boolean(options.headless);
  const command = headless
    ? join(dirname(merged.appPath), process.platform === 'win32' ? 'hython.exe' : 'hython')
    : merged.appPath;
  if (!existsSync(command)) throw codedError(`Houdini executable does not exist: ${command}`, 'APP_NOT_FOUND');
  const args = headless ? [paths.headlessRunner] : [];
  const ownedEnvironment = {
    HOUDINI_CLI_AUTOSTART: '1',
    HOUDINI_CLI_MCP_SOURCE: source,
    HOUDINI_CLI_MCP_HOST: merged.host,
    HOUDINI_CLI_MCP_PORT: String(merged.port),
    HOUDINI_PATH: houdiniPathWithOwnedStartup(paths.pluginPath, process.env.HOUDINI_PATH),
  };

  if (options.dryRun) {
    return { pid: null, dryRun: true, command, args, env: ownedEnvironment, headless };
  }

  if (await canConnect(merged.host, merged.port)) {
    throw codedError(`${merged.host}:${merged.port} is already accepting connections; refusing to launch a second Houdini bridge.`, 'PORT_IN_USE');
  }

  const spawn = options.spawn ?? spawnProcess;
  const logsDir = join(merged.stateDir, 'logs');
  mkdirSync(logsDir, { recursive: true });
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const logPath = join(logsDir, `houdini-${timestamp}.log`);
  const logFd = openSync(logPath, 'a');
  let child;
  try {
    child = spawn(command, args, {
      cwd: dirname(command),
      detached: true,
      env: { ...process.env, ...ownedEnvironment },
      shell: false,
      stdio: ['ignore', logFd, logFd],
      windowsHide: true,
    });
    const spawnError = await new Promise((resolveSpawn) => {
      child.once('error', resolveSpawn);
      child.once('spawn', () => resolveSpawn(null));
    });
    if (spawnError) throw spawnError;
  } catch (error) {
    throw codedError(`Failed to launch Houdini: ${error.message}`, 'LAUNCH_FAILED');
  } finally {
    closeSync(logFd);
  }

  try {
    await waitForBridge(child, merged.host, merged.port, Number(options.timeout ?? 15_000));
  } catch (error) {
    error.details = { ...(error.details ?? {}), pid: child.pid, logPath };
    throw error;
  } finally {
    child.unref?.();
  }
  return { pid: child.pid, command, args, host: merged.host, port: merged.port, headless, logPath };
}

export async function server(config) {
  const merged = mergedConfig(config);
  const paths = pathsFor(merged);
  if (!existsSync(join(paths.runtimeDir, 'pyproject.toml')) || !existsSync(paths.bridgePath) || !existsSync(paths.pythonPath)) {
    throw codedError('The isolated Houdini MCP runtime is missing. Run setup first.', 'NOT_SETUP');
  }
  return {
    command: paths.pythonPath,
    args: [paths.bridgePath, '--port', String(merged.port)],
    env: { PYTHONUNBUFFERED: '1' },
    cwd: paths.runtimeDir,
  };
}
