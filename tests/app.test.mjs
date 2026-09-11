import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import net from 'node:net';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { doctor, launch, metadata, server, setup } from '../src/app.mjs';

const houdiniExecutable = process.platform === 'win32' ? 'houdini.exe' : 'houdini';
const hythonExecutable = process.platform === 'win32' ? 'hython.exe' : 'hython';

function temporaryDirectory(t) {
  const directory = mkdtempSync(join(tmpdir(), 'houdini-cli-test-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  return directory;
}

function fixtureSource(root, bridge = 'import sys\nfrom langchain.output_parsers import ResponseSchema, StructuredOutputParser\n') {
  const source = join(root, 'external-source');
  mkdirSync(source, { recursive: true });
  writeFileSync(join(source, '__init__.py'), 'def start_server(host, port):\n    return None\n', 'utf8');
  writeFileSync(join(source, 'server.py'), '', 'utf8');
  writeFileSync(join(source, 'HoudiniMCPRender.py'), '', 'utf8');
  writeFileSync(join(source, 'houdini_mcp_server.py'), bridge, 'utf8');
  return source;
}

function fakeExec(calls) {
  return (command, args) => {
    calls.push({ command, args: [...args] });
    if (command === 'where.exe' || command === 'which') return `${process.execPath}\n`;
    if (args[0] === 'sync') {
      const runtime = args[args.indexOf('--project') + 1];
      const python = join(runtime, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
      mkdirSync(dirname(python), { recursive: true });
      writeFileSync(python, '', 'utf8');
    }
    return '';
  };
}

async function unusedPort() {
  const listener = net.createServer();
  await new Promise((resolveListen) => listener.listen(0, '127.0.0.1', resolveListen));
  const { port } = listener.address();
  await new Promise((resolveClose) => listener.close(resolveClose));
  return port;
}

test('metadata includes the targeted legacy Codex MCP names', () => {
  assert.deepEqual(metadata, {
    id: 'houdini-cli',
    bin: 'houdini-cli',
    label: 'Houdini',
    defaultPort: 9877,
    mcpNames: ['houdini-mcp', 'houdini'],
  });
});

test('setup dry-run plans a pinned download without touching the state directory', async (t) => {
  const root = temporaryDirectory(t);
  const stateDir = join(root, 'state');
  const result = await setup({ stateDir }, { dryRun: true });

  assert.equal(result.dryRun, true);
  assert.equal(result.config.sourceOwned, true);
  assert.match(result.plan[0], /de4fd93acc207fc57c02b330d421461f5963a945/);
  assert.equal(existsSync(stateDir), false);
});

test('setup discovers the numerically newest Houdini installation', async (t) => {
  const root = temporaryDirectory(t);
  const previousProgramFiles = process.env.ProgramFiles;
  const previousProgramFilesX86 = process.env['ProgramFiles(x86)'];
  t.after(() => {
    if (previousProgramFiles === undefined) delete process.env.ProgramFiles;
    else process.env.ProgramFiles = previousProgramFiles;
    if (previousProgramFilesX86 === undefined) delete process.env['ProgramFiles(x86)'];
    else process.env['ProgramFiles(x86)'] = previousProgramFilesX86;
  });
  process.env.ProgramFiles = root;
  process.env['ProgramFiles(x86)'] = '';
  for (const version of ['21.5.999', '22.0.9', '22.0.10']) {
    const executable = join(root, 'Side Effects Software', `Houdini ${version}`, 'bin', houdiniExecutable);
    mkdirSync(dirname(executable), { recursive: true });
    writeFileSync(executable, '', 'utf8');
  }

  const result = await setup({ stateDir: join(root, 'state') }, { dryRun: true, execFileSync: fakeExec([]) });
  assert.equal(result.config.appPath, join(root, 'Side Effects Software', 'Houdini 22.0.10', 'bin', houdiniExecutable));
});

test('setup keeps external source unchanged and patches only the generated bridge', async (t) => {
  const root = temporaryDirectory(t);
  const source = fixtureSource(root);
  const stateDir = join(root, 'state');
  const original = readFileSync(join(source, 'houdini_mcp_server.py'), 'utf8');
  const calls = [];

  const result = await setup(
    { stateDir, source, appPath: join(root, 'houdini.exe'), uvPath: 'uv' },
    { execFileSync: fakeExec(calls) },
  );

  assert.equal(result.config.source, source);
  assert.equal(result.config.sourceOwned, false);
  assert.equal(readFileSync(join(source, 'houdini_mcp_server.py'), 'utf8'), original);
  const generated = readFileSync(result.config.bridgePath, 'utf8');
  assert.match(generated, /langchain_classic\.output_parsers/);
  assert.deepEqual(result.patches, ['prefer-langchain-classic-output-parsers']);
  assert.match(readFileSync(join(result.config.runtimePath, 'pyproject.toml'), 'utf8'), /mcp\[cli\]==1\.4\.1/);
  assert.equal(calls.some(({ args }) => args[0] === 'sync' && args.includes(result.config.runtimePath)), true);
  assert.equal(calls.some(({ args }) => args[0] === '-c' && args.some((arg) => arg.includes('runpy.run_path'))), true);
});

test('server starts the generated bridge from the isolated uv project', async (t) => {
  const root = temporaryDirectory(t);
  const source = fixtureSource(root, 'from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser\n');
  const result = await setup(
    { stateDir: join(root, 'state'), source, uvPath: 'uv' },
    { execFileSync: fakeExec([]) },
  );

  const command = await server(result.config);
  assert.equal(command.command, result.config.pythonPath);
  assert.deepEqual(command.args, [result.config.bridgePath, '--port', '9877']);
  assert.equal(command.cwd, result.config.runtimePath);
  assert.deepEqual(command.env, { PYTHONUNBUFFERED: '1' });
});

test('launch dry-run adds a process-scoped Houdini path and never edits preferences', async (t) => {
  const root = temporaryDirectory(t);
  const source = fixtureSource(root);
  const bin = join(root, 'Houdini', 'bin');
  const appPath = join(bin, 'houdini.exe');
  mkdirSync(dirname(appPath), { recursive: true });
  writeFileSync(appPath, '', 'utf8');
  writeFileSync(join(bin, hythonExecutable), '', 'utf8');
  const configured = await setup(
    { stateDir: join(root, 'state'), source, appPath, uvPath: 'uv' },
    { execFileSync: fakeExec([]) },
  );

  const gui = await launch(configured.config, { dryRun: true });
  assert.equal(gui.command, appPath);
  assert.deepEqual(gui.args, []);
  assert.equal(gui.env.HOUDINI_CLI_AUTOSTART, '1');
  assert.equal(gui.env.HOUDINI_CLI_MCP_SOURCE, source);
  assert.ok(gui.env.HOUDINI_PATH.startsWith(configured.config.pluginPath));
  assert.ok(gui.env.HOUDINI_PATH.endsWith('&'));

  const headless = await launch(configured.config, { dryRun: true, headless: true });
  assert.equal(headless.command, join(bin, hythonExecutable));
  assert.deepEqual(headless.args, [join(configured.config.pluginPath, 'headless_runner.py')]);
  const runner = readFileSync(headless.args[0], 'utf8');
  assert.ok(runner.indexOf('QCoreApplication.instance()') < runner.indexOf('existing_module.stop_server()'));
  assert.ok(runner.indexOf('existing_module.stop_server()') < runner.indexOf('runpy.run_path'));
});

test('doctor reports an installed runtime without mutating it', async (t) => {
  const root = temporaryDirectory(t);
  const source = fixtureSource(root);
  const bin = join(root, 'bin');
  const appPath = join(bin, 'houdini.exe');
  mkdirSync(bin, { recursive: true });
  writeFileSync(appPath, '', 'utf8');
  writeFileSync(join(bin, hythonExecutable), '', 'utf8');
  const configured = await setup(
    { stateDir: join(root, 'state'), source, appPath, uvPath: 'uv' },
    { execFileSync: fakeExec([]) },
  );

  const result = await doctor(configured.config, { execFileSync: fakeExec([]), probeRuntime: false });
  assert.equal(result.ok, true);
  assert.equal(result.checks.every((item) => typeof item.name === 'string' && typeof item.ok === 'boolean' && typeof item.detail === 'string'), true);
});

test('launch converts an asynchronous spawn failure into a coded error and keeps a log', async (t) => {
  const root = temporaryDirectory(t);
  const source = fixtureSource(root);
  const bin = join(root, 'bin');
  const appPath = join(bin, 'houdini.exe');
  mkdirSync(bin, { recursive: true });
  writeFileSync(appPath, '', 'utf8');
  const configured = await setup(
    { stateDir: join(root, 'state'), source, appPath, uvPath: 'uv', port: await unusedPort() },
    { execFileSync: fakeExec([]) },
  );
  const child = new EventEmitter();
  child.pid = undefined;
  child.exitCode = null;
  child.unref = () => {};
  const spawn = () => {
    queueMicrotask(() => child.emit('error', new Error('synthetic spawn failure')));
    return child;
  };

  await assert.rejects(
    launch(configured.config, { spawn, timeout: 1000 }),
    (error) => error.code === 'LAUNCH_FAILED' && /synthetic spawn failure/.test(error.message),
  );
  assert.equal(existsSync(join(configured.config.stateDir, 'logs')), true);
});

test('setup rejects a non-loopback host with a coded error', async (t) => {
  const root = temporaryDirectory(t);
  await assert.rejects(
    setup({ stateDir: join(root, 'state'), host: '0.0.0.0' }, { dryRun: true }),
    (error) => error.code === 'HOST_NOT_LOOPBACK',
  );
});
