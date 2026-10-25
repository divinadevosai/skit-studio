"""Step 4: room tone + music (low) + every line at its start time + a blip for each pop-up."""
import json, os, subprocess, sys
from common import ffmpeg

ep_dir = sys.argv[1]; music = sys.argv[2] if len(sys.argv) > 2 else ''
build = os.path.join(ep_dir, 'build'); FF = ffmpeg()
tl = json.load(open(os.path.join(build, 'timeline.json'), encoding='utf-8')); total = tl['total']
args = [FF, '-loglevel', 'error', '-y', '-f', 'lavfi', '-t', str(total), '-i', 'anoisesrc=color=brown:amplitude=0.02:sample_rate=44100']
filters = ['[0:a]lowpass=f=400,volume=0.5[a0]']; labels = ['[a0]']; n = 1
if music:
    args += ['-i', music]
    filters.append(f'[1:a]lowpass=f=6000,aecho=0.8:0.5:120|260:0.3|0.2,volume=0.13[a1]'); labels.append('[a1]'); n = 2
for l in tl['lines']:
    args += ['-i', l['file']]; ms = int(l['start'] * 1000)
    filters.append(f'[{n}:a]adelay={ms}|{ms}[a{n}]'); labels.append(f'[a{n}]'); n += 1
    if l.get('pop'):
        args += ['-f', 'lavfi', '-t', '0.18', '-i', 'sine=frequency=1320:sample_rate=44100']
        filters.append(f'[{n}:a]afade=t=out:st=0.02:d=0.16,volume=0.15,adelay={ms + 150}|{ms + 150}[a{n}]'); labels.append(f'[a{n}]'); n += 1
filters.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.95,atrim=0:{total}[out]')
args += ['-filter_complex', ';'.join(filters), '-map', '[out]', '-ac', '2', '-ar', '44100', os.path.join(build, 'mix.wav')]
subprocess.run(args, check=True)
print('  mixed')
