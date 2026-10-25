"""Step 2: tidy each line (trim, short pauses, the host's AI effect, even loudness) and time the episode."""
import json, math, os, shutil, subprocess, sys
from common import load, ffmpeg, read_mono

project_dir, ep_dir = sys.argv[1], sys.argv[2]
raw_dir = sys.argv[3] if len(sys.argv) > 3 else None  # your own recordings, named l00.wav, l01.wav, ...
project, episode, build = load(project_dir, ep_dir)
FF = ffmpeg(); FPS = 30
effect = project.get('hostEffect', 'ai')
TRIM = ('silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.12:'
        'stop_threshold=-45dB:stop_silence=0.12')
AI = 'highpass=f=110,equalizer=f=4000:t=q:w=1:g=4,aecho=0.8:0.55:14:0.3,aecho=0.8:0.4:45:0.12'
t, out = 0.5, []
for i, line in enumerate(episode['lines']):
    folder = raw_dir or os.path.join(build, 'raw')
    # your own recordings can be any common format: l00.wav, l00.m4a (iPhone), l00.mp3 ...
    found = [os.path.join(folder, f'l{i:02d}{ext}') for ext in ('.wav', '.m4a', '.mp3', '.aac', '.ogg', '.flac', '.webm')]
    found = [f for f in found if os.path.exists(f)]
    if not found:
        sys.exit(f'Missing the recording for line {i} (l{i:02d}.wav, .m4a or .mp3) in {folder}')
    src = found[0]
    dst = os.path.join(build, f'v{i:02d}.wav')
    chain = [TRIM]
    if raw_dir: chain.append('atempo=1.06')  # Piper is already sped up at the source
    chain.append(AI if line['who'] == 'host' and effect == 'ai' else 'highpass=f=80')
    chain.append('loudnorm=I=-17:TP=-2')
    subprocess.run([FF, '-loglevel', 'error', '-y', '-i', src, '-af', ','.join(chain), '-ar', '44100', '-ac', '1', dst], check=True)
    s, sr = read_mono(dst); dur = len(s) / sr; hop = sr // FPS
    # loudness per video frame drives the mouths
    env = [round(min(1, math.sqrt(sum(x * x for x in s[k:k + hop]) / max(1, len(s[k:k + hop]))) / 5000), 3) for k in range(0, len(s), hop)]
    out.append({**line, 'start': round(t, 3), 'dur': round(dur, 3), 'env': env, 'file': dst})
    t += dur + min(line.get('gap', 0.12), 0.6)
total = t + float(project.get('endCardSeconds', 3.2))
json.dump({'fps': FPS, 'total': round(total, 2), 'lines': out, 'pops': episode.get('pops', {})},
          open(os.path.join(build, 'timeline.json'), 'w', encoding='utf-8'))
print(f'  timed: {total:.1f} s')
