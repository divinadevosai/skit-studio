# Skit Studio

A [Claude Code](https://claude.com/claude-code) skill that makes short explainer skits about your product: a confused low-poly human asks the questions real people ask, and a smug AI made of beads roasts them and explains, with pop-up cards showing the real thing. Vertical 1080×1920 video, ready for TikTok, Instagram Reels and YouTube Shorts, with the captions for all three written for you.

You design your own two characters and your own room. Claude writes each episode from your product's real docs, shows you the script, then voices it, renders it and writes the captions.

Made by [SWE3WE](https://swe3we.dev), and used for the Divina and Obstat skits.

## What you need

- [Claude Code](https://claude.com/claude-code)
- [Node.js](https://nodejs.org) 20 or newer
- [Python](https://python.org) 3.10 or newer (on Windows, tick "Add python.exe to PATH" when installing)
- About 600 MB of disk space for the browser, voice model and tools. A graphics card makes rendering much faster, but isn't required.

## Install

Put the skill in your Claude Code skills folder and install its parts:

**Windows (PowerShell)**
```
git clone https://github.com/divinadevosai/skit-studio "$HOME\.claude\skills\skit-studio"
cd "$HOME\.claude\skills\skit-studio"; npm install
```

**Mac or Linux**
```
git clone https://github.com/divinadevosai/skit-studio ~/.claude/skills/skit-studio
cd ~/.claude/skills/skit-studio && npm install
```

## Use it

Make a folder for your skits, open Claude Code in it and ask:

```
mkdir my-skits; cd my-skits
claude
> make me a skit about my product
```

The first time, Claude sets up the voice engine, asks about your product and your characters, and plays you some voices to pick from. After that, each new episode is one request: "make an episode about the export feature", or "a new repo is trending, make an episode about it and how it works with my product".

Every episode goes:
1. **Script:** Claude reads your product's docs and writes 10–14 lines. You approve or change them.
2. **Preview:** still frames, so you can check the pop-ups.
3. **Video:** voices (Piper, on your computer), music, render, saved as `video.mp4`.
4. **Captions:** `captions.md` with TikTok, Instagram and YouTube versions.

You can also record the lines yourself and use those instead.

## Your characters

Everything about the look is in `project.json`:
- **The guest:** skin, hair and hairstyle, beard, top, kilt or trousers (with your own tartan), hat (tam, beanie or cap) and glasses.
- **The host:** its bead colours and eye colour.
- **The room:** the corkboard notes and the mug.
- **The voices:** over 100 British and other accents in one voice model.

All the options are in [reference/project.md](reference/project.md), and [examples/obstat](examples/obstat) is a complete project with one episode.

## Credits and licences

- The code is under the [MIT licence](LICENSE).
- Fonts: Fraunces, Instrument Sans and JetBrains Mono, under the SIL Open Font License ([engine/fonts](engine/fonts)).
- Voices: [Piper](https://github.com/OHF-Voice/piper1-gpl) (installed on your computer, GPL-3.0) with the VCTK voice model. Videos that use the VCTK voices should credit "Voices: Piper TTS, VCTK corpus (CC BY 4.0)"; Claude adds this to your captions.
- The music is generated fresh for every episode, so it's yours to use.
- Rendering uses [three.js](https://threejs.org) (MIT), [Playwright](https://playwright.dev) (Apache-2.0) and [ffmpeg](https://ffmpeg.org) via [ffmpeg-static](https://github.com/eugeneware/ffmpeg-static) (GPL builds).

You're responsible for what your skits say about your product and anyone else's. The skill tells Claude to stick to facts from your docs, but check every script before you make it.
