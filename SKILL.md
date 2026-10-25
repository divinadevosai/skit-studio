---
name: skit-studio
description: Write, voice and render short two-character explainer skits (vertical 1080×1920 video) about the user's product, with captions for TikTok, Instagram Reels and YouTube Shorts. A low-poly human guest asks the questions real people ask, an AI host made of beads roasts them and explains, with pop-up cards showing the product. Use when the user wants a skit, explainer video, reel, short or TikTok about their product, a new episode of their skit series, or to set up their own characters.
---

# Skit Studio

You make one episode at a time: script → the user approves it → voices → video → captions. Everything runs on the user's computer.

The folder this file is in is the **skill folder** (call it `$SKILL`). The user's **project folder** holds their `project.json`, their voice model and one folder per episode:

```
my-skits/                 ← project folder (anywhere the user likes)
  project.json            ← characters, room, product, voices
  voices/                 ← the Piper voice model (made by setup)
  episodes/
    ep01/
      episode.json        ← the script and its pop-ups (you write this)
      screenshot.png      ← any images the pop-ups use
      video.mp4           ← the result
      captions.md         ← TikTok, Instagram and YouTube captions
```

Run every command **from the project folder**: `node "$SKILL/scripts/make.mjs" episodes/ep01`.

## 1. First time only: setup

1. Check `node --version` (20 or newer) and Python (`python --version` on Windows, `python3 --version` elsewhere; 3.10 or newer). If one is missing, tell the user where to get it (nodejs.org, python.org with "Add to PATH" ticked) and stop.
2. If `$SKILL/node_modules` doesn't exist, run `npm install` in `$SKILL`.
3. From the project folder, run `node "$SKILL/scripts/setup.mjs"`. It installs Piper (the voice engine) and numpy, downloads the voice model (about 75 MB) and installs the browser that renders the video.

## 2. First time only: the characters (project.json)

If the project folder has no `project.json`, interview the user. Ask in plain words, a few questions at a time. Offer sensible defaults; don't make them design everything.

- **The product:** name, website, one-line tagline, the button text for the end card ("Try it free"), an accent colour, and links to its docs, README or website. **Read those docs yourself**; every claim in every episode comes from them.
- **The host** (the AI made of beads): its name, its personality (default: smug, impatient and clever, roasts the guest, then explains properly) and its colours (`shadow`, `lit`, `eyes`; default is a blue).
- **The guest** (the low-poly human): skin, hair colour and style, beard, top, kilt or trousers, hat, glasses, and their personality (default: friendly, confused, asks what real people ask).
- **The room:** up to five corkboard notes (short, two lines each, ideally in-jokes about the product) and the mug text.
- **Pronunciations:** any name the voice will say wrong, spelled how it sounds (`"Divina": "Deevena"`).
- **Style:** emojis in captions, yes or no.

Write `project.json` using `$SKILL/templates/project.json` as the shape. Every option is listed in `$SKILL/reference/project.md`.

Then choose the voices: run `node "$SKILL/scripts/py.mjs" audition.py . scottish-male` (groups: `scottish-male`, `english-male`, `english-female`, `irish`, `american`; no group plays a selection of all of them). The user listens to the clips in `auditions/` and tells you which two to use. Put them in `voices.guest` and `voices.host`.

Finally, render one preview frame (see step 4) so the user sees their characters before the first full episode.

## 3. Write the episode

Make a new folder under `episodes/` and write `episode.json`. Its format and the pop-up types are in `$SKILL/reference/episode.md`, and `$SKILL/examples/obstat/` has a complete working episode.

**Shape of a good episode**
- 45 to 60 seconds, 10 to 14 lines, guest and host taking turns. The guest opens with a question in the first line; nobody wants a slow intro.
- One topic per episode: one feature, or one trend tied back to the product.
- The guest asks the obvious, slightly dumb question a real viewer would ask. The host roasts them (one short jab), then explains clearly and concretely.
- 4 to 6 pop-ups, each showing the thing being said at that moment. The last line has the `end` pop-up.
- End on a punchline, then the end card.
- Lines are short and spoken. Write them for the ear: no lists of more than three things, no brackets, no URLs read out.

**Trend episodes** ("a new repo dropped", "everyone's talking about X"): search for what's trending, then **read the trending thing's own README or docs** before writing anything about it. Only connect it to the user's product in ways the product's docs actually support. Tell the user where each claim about the trend came from.

**Rules that always apply**
- **Every claim about the product must be in its docs.** Don't invent features, numbers, prices, platforms, user counts or reviews. If you're not sure the product does something, ask the user.
- **Never imply that another company, product or person endorses the user's product.** Naming a real tool you're explaining is fine; putting a real project on a pop-up as an example of the user's product (a "reviewed" list, a "customers" list) is not. Use made-up generic names there.
- **Roasts are playful, never cruel.** Tease the guest's confusion, never their nationality, accent, looks, gender, religion, body or anything else about who they are. The guest's accent and clothes are part of the character, not the joke.
- Keep it platform-safe: no swearing beyond "idiot" level, nothing sexual, nothing dangerous.

Show the user the script as a table (number, who, line, pop-up) and **wait for approval** before making anything. Change lines they want changed.

## 4. Make it

From the project folder:

1. **Preview first:** `node "$SKILL/scripts/make.mjs" episodes/ep01 --preview 3,15,30,45`. It writes `preview-<seconds>.jpg` in the episode folder. Look at them: is any pop-up hiding the host's face, is text cut off, is anything wrong? Fix `episode.json` and preview again. Show the user one or two previews.
2. **The full video:** `node "$SKILL/scripts/make.mjs" episodes/ep01`. It writes `episodes/ep01/video.mp4`. It takes a few minutes with a graphics card and longer without one. Run it in the background if you can, and tell the user roughly how long it'll take.

Options:
- `--voices <folder>` uses the user's own recordings (`l00.wav`, `l01.wav`, … in script order) instead of Piper. Use this if they recorded the lines themselves or made them with another voice tool.
- `--no-music` leaves out the music bed.
- If the voice says a word wrong, add it to `pronounce` in `project.json`, or give that line a `say` field with the spoken version (the caption still shows `text`).

If something fails, read the error. The most common fixes are in `$SKILL/reference/troubleshooting.md`.

## 5. Captions

Write `captions.md` in the episode folder with three sections. Follow the user's emoji preference from `project.json` (`style.emoji`).

**TikTok**
- A hook line first, usually "POV: …" or the funniest line of the skit.
- One or two short lines saying what the product does, using only facts from the episode.
- "Link in bio" (or "pinned comment" for new accounts).
- The credit line from `project.json`.
- 5 to 8 hashtags.
- A suggested **pinned comment** with the link.

**Instagram Reels**
- A hook line.
- Two or three sentences on what the product does.
- "Link in bio."
- The credit line.
- 3 to 5 hashtags.

**YouTube Shorts**
- A **title** under 60 characters.
- A **description** with what the product does, the link written out, the credit line, and hashtags with `#shorts` first (the first three show above the title).
- A pinned comment with the link (description links aren't clickable on phones).

The voices from the VCTK voice model need credit (CC BY 4.0): always include the `credit` line from `project.json` in every caption. The music is generated fresh for each episode, so it needs no credit.

## 6. Hand it over

Tell the user where `video.mp4` and `captions.md` are, show the captions in your reply so they can copy them, and suggest a posting time (6–9pm in their timezone) and the first-hour habit (reply to every comment).
