# episode.json

```json
{
  "title": "What are AI skills?",
  "lines": [
    { "who": "guest", "text": "What even is a skill?", "shot": "guest" },
    { "who": "host", "text": "A little instruction pack for an AI agent.", "shot": "host", "pop": "skills", "smug": true }
  ],
  "pops": {
    "skills": { "type": "list", "title": "What is a skill?", "items": [{ "text": "review-code" }] },
    "end": { "type": "end" }
  }
}
```

## Lines
| Key | What it does |
|---|---|
| `who` | `guest` or `host`. |
| `text` | What's said and shown as the caption. |
| `say` | Optional: a different spelling for the voice only ("Build a U.I."). |
| `caption` | Optional: different caption text from what's said. |
| `shot` | The camera: `guest`, `host`, `wide` (both) or `tv` (the guest looks at the TV on the shelf; good for "wait, how do you know that?" beats). |
| `pop` | Optional: the id of a pop-up in `pops`. It appears when this line starts and stays until two lines later. |
| `smug` | Host only: the host tilts its head and narrows its eyes after the roast. |
| `gap` | Optional: seconds of pause after the line (default 0.12, at most 0.6). Use it before a punchline. |

Put pop-ups on host lines with the `host` shot: they show full size there and shrink into the top corner on other shots.

## Pop-up types
Every text field is optional, and long text shrinks to fit.

**`image`**: a screenshot of the product.
`{ "type": "image", "title": "APP · what you're looking at", "image": "screenshot.png", "button": "Install ✓" }`
The image goes in the episode folder, ideally 16:10 (it's cropped to fit 840×525).

**`list`**: up to 4 rows, each with a mark (`check`, `cross` or `dot`) and an optional note. A `cross` row gets struck through.
`{ "type": "list", "title": "The reviewed list", "subtitle": "…", "items": [{ "text": "image-studio", "note": "checked", "mark": "check" }, { "text": "sketchy-repo", "note": "removed", "mark": "cross" }] }`

**`tiles`**: up to 3 cards side by side, with an optional green footer line.
`{ "type": "tiles", "title": "One folder per app", "items": [{ "title": "chat-bot", "lines": ["own Python", "own Node"] }], "footer": "nothing clashes" }`

**`terminal`**: a repo or tool with its command, and chips under it. `lastAccent` colours the last chip.
`{ "type": "terminal", "kicker": "trending on GitHub", "title": "owner / repo", "subtitle": "what it is", "command": "npx something", "chips": ["Works with A", "B", "+20 more"], "lastAccent": true }`

**`button`**: one big button being pressed, then a line underneath.
`{ "type": "button", "kicker": "APP", "title": "owner/repo", "subtitle": "installed", "button": "Build a UI", "after": "reading --help …" }`

**`form`**: up to 3 labelled fields, an optional checkbox and a Run button.
`{ "type": "form", "title": "tool", "subtitle": "a screen made from its options", "fields": [["Source", "owner/repo"]], "check": "Install everywhere", "button": "Run" }`

**`end`**: the end card, from `product` in project.json. You can override `name`, `tagline`, `cta`, `url` and `footnote` here.
`{ "type": "end" }`
