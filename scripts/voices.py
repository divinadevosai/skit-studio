"""Step 1: speak every line with Piper (or espeak-ng as a fallback) into build/raw/lNN.wav."""
import json, os, re, subprocess, sys
from common import load

project_dir, ep_dir = sys.argv[1], sys.argv[2]
project, episode, build = load(project_dir, ep_dir)
V = {'engine': 'piper', 'model': 'en_GB-vctk-medium', 'dir': 'voices', 'guest': 'p271', 'host': 'p254',
     'lengthScale': 0.93, 'sentenceSilence': 0.12, **project.get('voices', {})}
pronounce = project.get('pronounce', {})

def spoken(line):
    text = line.get('say') or line['text']
    for word, sound in pronounce.items():  # brand names the voice gets wrong, e.g. "Divina": "Deevena"
        text = re.sub(rf'\b{re.escape(word)}\b', sound, text)
    return text

if V['engine'] == 'piper':
    vdir = os.path.join(project_dir, V['dir'])
    model = os.path.join(vdir, V['model'] + '.onnx')
    if not os.path.exists(model):
        sys.exit(f'No voice model at {model}. Run "npm run setup" first.')
    speakers = json.load(open(model + '.json', encoding='utf-8')).get('speaker_id_map', {})
    def sid(name):
        if name in speakers: return str(speakers[name])
        if str(name).isdigit(): return str(name)
        sys.exit(f'Speaker "{name}" is not in {V["model"]}. Run "npm run audition" to hear the options.')
    py = os.environ.get('PYTHON', sys.executable)
    for i, line in enumerate(episode['lines']):
        out = os.path.join(build, 'raw', f'l{i:02d}.wav')
        cmd = [py, '-m', 'piper', '-m', model, '-s', sid(V[line['who']]), '-f', out,
               '--length-scale', str(V['lengthScale']), '--sentence-silence', str(V['sentenceSilence'])]
        # the text goes in on stdin, so quotes and apostrophes never need escaping
        subprocess.run(cmd, input=spoken(line).encode('utf-8'), check=True)
        print(f'  voice {i:02d} {line["who"]}')
elif V['engine'] == 'espeak':
    voice = {'guest': V.get('espeakGuest', 'en-gb-scotland'), 'host': V.get('espeakHost', 'en-gb-x-rp')}
    for i, line in enumerate(episode['lines']):
        out = os.path.join(build, 'raw', f'l{i:02d}.wav')
        subprocess.run(['espeak-ng', '-v', voice[line['who']], '-s', '165', '-w', out, spoken(line)], check=True)
        print(f'  voice {i:02d} {line["who"]} (espeak)')
else:
    sys.exit(f'Unknown voice engine "{V["engine"]}": use "piper" or "espeak"')
