#!/usr/bin/env node
// Runs one of the Python scripts with the right Python for this computer: node scripts/py.mjs audition.py [args]
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const PY = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const [script, ...rest] = process.argv.slice(2);
const r = spawnSync(PY, [path.join(path.dirname(fileURLToPath(import.meta.url)), script), ...(rest.length ? rest : [(process.env.INIT_CWD || process.cwd())])], { stdio: 'inherit', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
process.exit(r.status ?? 1);
