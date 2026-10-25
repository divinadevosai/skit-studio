"""Shared helpers for the Python steps: paths, settings and reading WAV files."""
import json, os, sys, wave, struct

def load(project_dir, ep_dir):
    project = json.load(open(os.path.join(project_dir, 'project.json'), encoding='utf-8'))
    episode = json.load(open(os.path.join(ep_dir, 'episode.json'), encoding='utf-8'))
    build = os.path.join(ep_dir, 'build')
    os.makedirs(os.path.join(build, 'raw'), exist_ok=True)
    return project, episode, build

def ffmpeg():
    ff = os.environ.get('FFMPEG')
    if not ff:
        sys.exit('FFMPEG is not set: run this through scripts/make.mjs, which finds ffmpeg for you')
    return ff

def read_mono(path):
    w = wave.open(path)
    n, sr, ch, width = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    data = w.readframes(n); w.close()
    if width != 2:
        sys.exit(f'{path}: expected 16-bit audio')
    s = struct.unpack(f'<{n * ch}h', data)
    return list(s[::ch]), sr
