"""Step 3: a soft, original music bed (no licence needed): a slow chord pad with a quiet bell melody."""
import json, os, sys, wave
import numpy as np

ep_dir = sys.argv[1]; build = os.path.join(ep_dir, 'build')
total = json.load(open(os.path.join(build, 'timeline.json'), encoding='utf-8'))['total'] + 1
mood = sys.argv[2] if len(sys.argv) > 2 else 'calm'
SR = 44100; n = int(total * SR); t = np.arange(n) / SR; out = np.zeros((n, 2))
f = lambda m: 440 * 2 ** ((m - 69) / 12)
CHORDS = {'calm': [[45, 57, 60, 64, 71], [41, 53, 57, 60, 64], [48, 55, 60, 64, 69], [43, 55, 59, 62, 67]],
          'bright': [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]}[mood]
bar = 4.0; rng = np.random.default_rng(3)
for b in range(int(total / bar) + 2):
    st = b * bar; ch = CHORDS[b % 4]; i0 = int(st * SR); i1 = min(n, int((st + bar + 1.5) * SR))
    if i0 >= n: break
    tt = t[i0:i1] - st; env = np.clip(tt / 1.6, 0, 1) * np.clip((bar + 1.5 - tt) / 1.5, 0, 1)
    for k, m in enumerate(ch):
        for det, pan in ((-0.12, 0.3), (0.12, 0.7)):
            v = np.sin(2 * np.pi * f(m + det) * tt + k) * (0.5 if k == 0 else 0.22) * env * (1 + 0.15 * np.sin(2 * np.pi * 0.3 * tt + k))
            out[i0:i1, 0] += v * (1 - pan); out[i0:i1, 1] += v * pan
    for j in range(8):
        m = ch[1 + (j * 3) % 4] + 12; s0 = int((st + j * 0.5) * SR); s1 = min(n, s0 + int(1.8 * SR))
        if s0 >= n: break
        tb = t[s0:s1] - (st + j * 0.5); v = (np.sin(2 * np.pi * f(m) * tb) + 0.3 * np.sin(4 * np.pi * f(m) * tb)) * np.exp(-tb * 3.2) * 0.09
        pan = 0.3 + 0.4 * rng.random(); out[s0:s1, 0] += v * (1 - pan); out[s0:s1, 1] += v * pan
out /= np.abs(out).max(); out *= 0.8
out *= (np.clip(t / 2, 0, 1) * np.clip((total - t) / 2.5, 0, 1))[:, None]
w = wave.open(os.path.join(build, 'music.wav'), 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
print(f'  music: {total:.1f} s')
