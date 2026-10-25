# project.json

Everything is optional except `product.name`. Colours are hex (`"#ff8c3a"`).

## product
| Key | What it does |
|---|---|
| `name` | Shown big on the end card. |
| `tagline` | One line under the name. |
| `cta` | The end card's button text, e.g. "Try it free". |
| `url` | Shown under the button. Written as people should type it, without `https://`. |
| `accent` | The product's colour: end card, buttons and highlights on the pop-ups. |
| `footnote` | A small line at the bottom of the end card (optional). |
| `docs` | Links to the product's website, README or docs. Read them before writing any episode. |

## host (the AI made of beads)
| Key | Default | What it does |
|---|---|---|
| `name` | | What the guest calls the host. |
| `personality` | | For you, when writing lines. |
| `shadow` | `#071133` | Bead colour in shadow. Keep it dark. |
| `lit` | `#5c94ff` | Bead colour where the light hits. |
| `eyes` | `#e6f2ff` | The glowing eyes and mouth. |

Good pairs: blue `#071133`/`#5c94ff`, purple `#1a0833`/`#a46bff`, green `#03241a`/`#3cffb4`, gold `#2a1a05`/`#ffc45c`, red `#2a0508`/`#ff5c6b`.

## guest (the low-poly human)
| Key | Options | Default |
|---|---|---|
| `name`, `personality` | for you, when writing lines | |
| `skin` | any colour | `#e8b496` |
| `hair` | any colour (also the beard and eyebrows) | `#4a2c1a` |
| `hairStyle` | `short`, `long`, `bald` | `short` |
| `beard` | `none`, `moustache`, `short`, `big` | `none` |
| `top` | any colour | `#2f5a46` |
| `bottom` | `trousers`, `kilt` | `trousers` |
| `bottomColor` | trouser colour | `#2b3a55` |
| `tartan` | four colours: base, band, band, thin line (kilt and tam) | red tartan |
| `socks`, `shoes` | colours | cream, black |
| `hat` | `none`, `tam`, `beanie`, `cap` | `none` |
| `hatColor` | colour (the tam's pom-pom, the beanie, the cap) | red |
| `glasses` | `true` / `false` | `false` |

## room
| Key | What it does |
|---|---|
| `wall` | Wall colour. |
| `notes` | Up to five corkboard notes, each `["LINE ONE", "LINE TWO"]`. Short: about 12 characters a line. |
| `mug` | The mug's two lines. |

## voices
| Key | Default | What it does |
|---|---|---|
| `engine` | `piper` | `piper`, or `espeak` (robotic, but needs no download). |
| `model` | `en_GB-vctk-medium` | Any Piper voice model. The VCTK one has 100+ British and other accents in one file. |
| `dir` | `voices` | Where setup put the model, inside the project folder. |
| `guest`, `host` | `p271`, `p254` | Speaker names from the model. Find them with the audition script. |
| `lengthScale` | `0.93` | Below 1 speaks faster. |
| `sentenceSilence` | `0.12` | Seconds of pause after each sentence. |

## Other keys
| Key | What it does |
|---|---|
| `pronounce` | `{"Word": "how it sounds"}`, applied to every spoken line. |
| `hostEffect` | `ai` (speaker EQ, a metallic double, a small room) or `none`. |
| `captions` | `{"host": "#ffd84d", "guest": "#ffffff"}`: the on-screen caption colours. |
| `music` | `false` to leave it out. |
| `musicMood` | `calm` or `bright`. |
| `musicFile` | Your own music file instead (you must have the rights to it). |
| `endCardSeconds` | How long the end card stays (default 3.2). |
| `credit` | The voice credit for captions. Keep it if you use the VCTK model; for another Piper voice, use what its MODEL_CARD asks for. |
| `style.emoji` | Whether captions use emojis. |
| `handles` | The user's account names, for captions. |
