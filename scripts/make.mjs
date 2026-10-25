#!/usr/bin/env node
// node scripts/make.mjs <episode folder> [--project <folder>] [--voices <folder>] [--preview 3,12.5] [--no-music]
// Runs every step and writes <episode>/video.mp4. With --preview, writes still frames instead.
import { spawn, spawnSync } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const require = createRequire(import.meta.url);
const args = process.argv.slice(2);
const flag = (name) => { const i = args.indexOf(name); return i >= 0 ? args.splice(i, 2)[1] : undefined; };
const has = (name) => { const i = args.indexOf(name); if (i >= 0) args.splice(i, 1); return i >= 0; };
const preview = flag('--preview');
const HERE = process.env.INIT_CWD || process.cwd(); // npm runs scripts from the skill folder, so use where you typed the command
const voiceArg = flag('--voices'); const voicesDir = voiceArg && path.resolve(HERE, voiceArg);
const noMusic = has('--no-music');
const projectDir = path.resolve(HERE, flag('--project') || '.');
const epDir = path.resolve(HERE, args[0] || '');
if (!args[0] || !fs.existsSync(path.join(epDir, 'episode.json'))) { console.error('Usage, from your project folder: node <skill folder>/scripts/make.mjs <episode folder>  (it must contain episode.json)'); process.exit(1); }
if (!fs.existsSync(path.join(projectDir, 'project.json'))) { console.error(`No project.json in ${projectDir}. Run from your project folder, or pass --project <folder>.`); process.exit(1); }
const project = JSON.parse(fs.readFileSync(path.join(projectDir, 'project.json'), 'utf8'));
const FFMPEG = process.env.FFMPEG || require('ffmpeg-static');
const PY = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const env = { ...process.env, FFMPEG, PYTHON: PY, PYTHONIOENCODING: 'utf-8' };
const py = (script, ...rest) => { const r = spawnSync(PY, [path.join(ROOT, 'scripts', script), ...rest], { stdio: 'inherit', env }); if (r.status !== 0) process.exit(r.status || 1); };
const build = path.join(epDir, 'build');

// catch script mistakes now, not five minutes into a render
const POP_TYPES = ['image', 'list', 'tiles', 'terminal', 'button', 'form', 'end'];
const SHOT_NAMES = ['guest', 'host', 'wide', 'tv'];
const problems = [];
let episode;
try { episode = JSON.parse(fs.readFileSync(path.join(epDir, 'episode.json'), 'utf8')); } catch (e) { console.error('episode.json is not valid JSON: ' + e.message); process.exit(1); }
if (!Array.isArray(episode.lines) || !episode.lines.length) problems.push('"lines" must be a list with at least one line');
(episode.lines || []).forEach((l, i) => {
  if (!['guest', 'host'].includes(l.who)) problems.push(`line ${i}: "who" must be "guest" or "host"`);
  if (typeof l.text !== 'string' || !l.text.trim()) problems.push(`line ${i}: "text" is missing`);
  if (l.shot && !SHOT_NAMES.includes(l.shot)) problems.push(`line ${i}: unknown shot "${l.shot}" (use ${SHOT_NAMES.join(', ')})`);
  if (l.pop && !(episode.pops || {})[l.pop]) problems.push(`line ${i}: pop-up "${l.pop}" isn't in "pops"`);
});
for (const [id, p] of Object.entries(episode.pops || {})) {
  if (!POP_TYPES.includes(p.type)) problems.push(`pop-up "${id}": unknown type "${p.type}" (use ${POP_TYPES.join(', ')})`);
  if (p.image && !fs.existsSync(path.join(epDir, p.image))) problems.push(`pop-up "${id}": image ${p.image} isn't in the episode folder`);
}
if (problems.length) { console.error('Fix episode.json first:\n  ' + problems.join('\n  ')); process.exit(1); }

console.log('1/5 voices'); if (voicesDir) console.log('  using your recordings in ' + voicesDir); else py('voices.py', projectDir, epDir);
console.log('2/5 audio'); py('audio.py', projectDir, epDir, ...(voicesDir ? [path.resolve(voicesDir)] : []));
const musicFile = noMusic || project.music === false ? '' : project.musicFile ? path.resolve(projectDir, project.musicFile) : path.join(build, 'music.wav');
console.log('3/5 music'); if (musicFile === path.join(build, 'music.wav')) py('music.py', epDir, project.musicMood || 'calm'); else console.log(musicFile ? '  using ' + musicFile : '  none');
console.log('4/5 mix'); py('mix.py', epDir, musicFile);

// 5: render. A tiny local server gives the page the engine, three.js, the project and the episode.
console.log('5/5 render');
const THREE_DIR = path.join(ROOT, 'node_modules', 'three');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml' };
const inside = (base, rel) => { const f = path.resolve(base, '.' + path.sep + rel); return f.startsWith(base + path.sep) || f === base ? f : null; };
const server = http.createServer((q, res) => {
  if (q.method !== 'GET' || q.headers.host !== `127.0.0.1:${server.address().port}`) { res.writeHead(403); return res.end(); }
  let u; try { u = decodeURIComponent(q.url.split('?')[0]); } catch { res.writeHead(400); return res.end(); }
  let f = null;
  if (u.startsWith('/three/')) f = inside(THREE_DIR, u.slice(7));
  else if (u === '/project/project.json') f = path.join(projectDir, 'project.json');
  else if (u === '/ep/timeline.json') f = path.join(build, 'timeline.json');
  else if (u.startsWith('/ep/')) f = inside(epDir, u.slice(4));
  else f = inside(path.join(ROOT, 'engine'), u === '/' ? 'index.html' : u.slice(1));
  if (!f) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'content-type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream' }); res.end(d); });
}).listen(0, '127.0.0.1');
await new Promise((ok) => server.once('listening', ok));
const port = server.address().port;
if (process.env.SKIT_DEBUG) console.log('  local server on port ' + port);

const { chromium } = await import('playwright');
const soft = process.env.SKIT_SOFTWARE_GL === '1';
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  args: soft ? ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] : ['--ignore-gpu-blocklist', '--enable-gpu-rasterization'],
});
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const errors = []; page.on('pageerror', (e) => errors.push(e.message)); page.on('console', (m) => { if ((m.type() === 'error' || m.type() === 'warning') && !/favicon|404/.test(m.text())) errors.push(m.text()); });
await page.goto(`http://127.0.0.1:${port}/`);
await page.waitForFunction(() => window.__ready, null, { timeout: 180000 }).catch(() => { console.error('The page did not load:', errors.join('\n')); process.exit(1); });
const tl = JSON.parse(fs.readFileSync(path.join(build, 'timeline.json'), 'utf8'));

if (preview) {
  const times = preview.split(',').map(Number);
  // the camera and pop-ups ease between frames, so walk up to each time instead of jumping
  let t0 = 0;
  for (const t of times.sort((a, b) => a - b)) {
    for (let s = Math.max(t0, t - 1.5); s < t; s += 1 / tl.fps) await page.evaluate((s) => window.renderAt(s), s);
    const jpg = await page.evaluate((t) => window.frameAt(t), t);
    fs.writeFileSync(path.join(epDir, `preview-${t}.jpg`), Buffer.from(jpg, 'base64')); console.log(`  preview-${t}.jpg`); t0 = t;
  }
} else {
  const out = path.join(epDir, 'video.mp4');
  const ff = spawn(FFMPEG, ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(tl.fps), '-c:v', 'mjpeg', '-i', '-', '-i', path.join(build, 'mix.wav'),
    '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.ceil(tl.total * tl.fps); const start = Date.now();
  for (let i = 0; i < n; i++) {
    const jpg = await page.evaluate((t) => window.frameAt(t), i / tl.fps);
    if (!ff.stdin.write(Buffer.from(jpg, 'base64'))) await new Promise((ok) => ff.stdin.once('drain', ok));
    if (i % 60 === 0) process.stdout.write(`\r  frame ${i}/${n} · ${Math.round((Date.now() - start) / 1000)} s`);
  }
  ff.stdin.end(); await new Promise((ok) => ff.on('close', ok));
  console.log(`\r  done: ${out}                    `);
}
if (errors.length) console.warn('Page messages:\n' + errors.slice(0, 5).join('\n'));
await browser.close(); server.close();
