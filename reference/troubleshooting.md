# Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found (Windows) | Install Python from python.org with "Add python.exe to PATH" ticked, then open a new terminal. Or set `PYTHON` to the full path of python.exe. |
| `No voice model at …` | Run `node "$SKILL/scripts/setup.mjs"` from the project folder. |
| `Speaker "pXXX" is not in …` | That name isn't in the model. Run the audition script and pick from the clips it makes. |
| The voice says a name wrong | Add it to `pronounce` in project.json, spelled how it sounds. |
| The page didn't load / a black video | Run `npx playwright install chromium` in the skill folder. On a computer with no graphics card, set `SKIT_SOFTWARE_GL=1` (slower, but it works anywhere). |
| Rendering is very slow | Normal without a graphics card. Render overnight, or render previews only while you're writing. |
| A pop-up hides the host's face | Move the `pop` to a line with the `host` shot, or use fewer list items. |
| Text is tiny on a pop-up | It shrank to fit. Shorten it. |
| `FFMPEG is not set` | Run through `make.mjs`, not the Python scripts on their own. |
| Your own recordings are used but the timing is off | Name them `l00.wav`, `l01.wav`, … in exactly the order of `lines`, one file per line. |
