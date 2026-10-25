#!/usr/bin/env node
// npm run setup: installs the Python parts and the voice model, and checks the browser.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PY = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const projectDir = path.resolve(process.argv[2] || (process.env.INIT_CWD || process.cwd()));
const run = (cmd, a, what) => { console.log(`\n> ${what}`); const r = spawnSync(cmd, a, { stdio: 'inherit', shell: process.platform === 'win32' && cmd === 'npx' }); if (r.status !== 0) { console.error(`\n${what} failed. Fix the error above and run "npm run setup" again.`); process.exit(1); } };

const v = spawnSync(PY, ['--version'], { encoding: 'utf8' });
if (v.status !== 0) { console.error(`Python wasn't found as "${PY}". Install Python 3.10+ from python.org (tick "Add to PATH"), or set PYTHON to its path.`); process.exit(1); }
console.log('Python: ' + (v.stdout || v.stderr).trim());
run(PY, ['-m', 'pip', 'install', '-r', path.join(ROOT, 'requirements.txt')], 'Installing Piper and numpy');
let model = 'en_GB-vctk-medium', dir = 'voices';
const pj = path.join(projectDir, 'project.json');
if (fs.existsSync(pj)) { const p = JSON.parse(fs.readFileSync(pj, 'utf8')); model = p.voices?.model || model; dir = p.voices?.dir || dir; }
const vdir = path.join(projectDir, dir); fs.mkdirSync(vdir, { recursive: true });
if (!fs.existsSync(path.join(vdir, model + '.onnx'))) run(PY, ['-m', 'piper.download_voices', model, '--download-dir', vdir], `Downloading the ${model} voice (about 75 MB)`);
else console.log(`\nVoice ${model} is already in ${vdir}`);
if (!process.env.CHROMIUM_PATH) run('npx', ['playwright', 'install', 'chromium'], 'Installing the browser that renders the video');
console.log('\nAll set. Next: npm run audition, to pick the two voices.');
