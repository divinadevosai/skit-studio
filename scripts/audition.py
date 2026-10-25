"""node scripts/py.mjs audition.py <project folder> [group]: one sample clip per speaker, so you can pick a voice for each character."""
import json, os, subprocess, sys

SETUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.mjs')

project_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
p = {}
if os.path.exists(os.path.join(project_dir, 'project.json')):
    p = json.load(open(os.path.join(project_dir, 'project.json'), encoding='utf-8'))
V = {'model': 'en_GB-vctk-medium', 'dir': 'voices', **p.get('voices', {})}
model = os.path.join(project_dir, V['dir'], V['model'] + '.onnx')
if not os.path.exists(model):
    sys.exit(f'No voice model at {model}. Run setup first: node "{SETUP}"')
speakers = json.load(open(model + '.json', encoding='utf-8')).get('speaker_id_map', {}) or {'0': 0}
# VCTK speakers worth trying first, by accent (from the VCTK corpus speaker list)
PICKS = {'scottish-male': ['p237', 'p241', 'p246', 'p247', 'p252', 'p255', 'p263', 'p271', 'p272', 'p281', 'p284', 'p285'],
         'english-male': ['p226', 'p232', 'p254', 'p258', 'p273'],
         'english-female': ['p225', 'p228', 'p229', 'p230', 'p231'],
         'irish': ['p245', 'p298', 'p313', 'p340'],
         'american': ['p294', 'p299', 'p300', 'p301', 'p311', 'p360']}
group = sys.argv[2] if len(sys.argv) > 2 else None
names = PICKS.get(group, list(speakers)[:24]) if group else [n for g in PICKS.values() for n in g]
text = sys.argv[3] if len(sys.argv) > 3 else 'Right. So what does this thing actually do?'
out = os.path.join(project_dir, 'auditions'); os.makedirs(out, exist_ok=True)
for name in names:
    if name not in speakers: continue
    subprocess.run([sys.executable, '-m', 'piper', '-m', model, '-s', str(speakers[name]), '-f', os.path.join(out, f'{name}.wav')], input=text.encode('utf-8'), check=True)
    print(f'  {name}.wav')
print(f'\nListen in {out} and put the two you like in project.json under "voices": "guest" and "host".')
print('Groups: ' + ', '.join(PICKS) + f'   e.g. node "{os.path.join(os.path.dirname(SETUP), "py.mjs")}" audition.py . scottish-male')
