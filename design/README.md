# EDL GUI design tokens

The design system for the EDL GUI: colors for two themes, type, spacing, radii and the core components.

| File | What |
| --- | --- |
| `tokens.json` | The source of truth. Edit this. |
| `tokens.css` | CSS custom properties generated from `tokens.json`. Don't edit by hand. |
| `components.css` | Component classes (`edl-btn`, `edl-chip`, `edl-table`, …) built on the tokens. |
| `build_tokens.py` | Regenerates `tokens.css`: `python3 design/build_tokens.py` |
| `preview.html` | Every component on one page, with a theme switch. Open it in a browser. |

## Using it

```html
<link rel="stylesheet" href="design/tokens.css">
<link rel="stylesheet" href="design/components.css">
<body class="edl-root">
```

- **Themes:** Bench (dark) is the default. The page follows the OS setting unless the root element carries `data-theme="bench"` or `data-theme="board"`.
- **Fonts:** Chakra Petch, IBM Plex Sans and JetBrains Mono, loaded from Google Fonts by `components.css`. For an offline build, vendor the font files and replace the `@import`.
- **Type styles:** `.edl-type-display`, `-title`, `-body`, `-label`, `-mono`, `-log`.

A Qt (QSS) front end can read `tokens.json` directly; the color values are plain hex and aliases are written `{token-name}`.
