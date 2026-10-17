#!/usr/bin/env python3
"""Generate design/tokens.css from design/tokens.json.

Usage: python3 design/build_tokens.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALIAS = re.compile(r"^\{([A-Za-z0-9][A-Za-z0-9_.-]*)\}$")


def css_value(value):
    m = ALIAS.match(value)
    return f"var(--{m.group(1)})" if m else value


def color_block(tokens, theme, first):
    lines = []
    for tok in tokens:
        value = tok["value"]
        if isinstance(value, dict):
            value = value.get(theme, value.get(first))
        lines.append(f"  --{tok['name']}: {css_value(value)};")
    return lines


def main():
    t = json.loads((HERE / "tokens.json").read_text(encoding="utf-8"))
    themes = [th["id"] for th in t["color"]["themes"]]
    dark, light = themes[0], themes[1]
    colors = t["color"]["tokens"]

    out = [f"/* {t['name']} tokens. Generated from tokens.json by build_tokens.py; do not edit. */", ""]
    out.append(f':root, [data-theme="{dark}"] {{')
    out += color_block(colors, dark, dark)
    out += ["  color-scheme: dark;", "}", ""]
    out.append("@media (prefers-color-scheme: light) {")
    out.append(f'  :root:not([data-theme="{dark}"]) {{')
    out += ["  " + line for line in color_block(colors, light, dark)]
    out += ["    color-scheme: light;", "  }", "}", ""]
    out.append(f'[data-theme="{light}"] {{')
    out += color_block(colors, light, dark)
    out += ["  color-scheme: light;", "}", ""]

    out.append(":root {")
    for family in ("spacing", "radius"):
        for tok in t[family]["tokens"]:
            out.append(f"  --{tok['name']}: {tok['value']};")
    for key, stack in t["type"]["families"].items():
        out.append(f"  --font-{key}: {stack};")
    out += ["}", ""]

    for group in t["type"]["groups"]:
        for style in group["styles"]:
            family = style.get("family", group["family"])
            out.append(f".edl-type-{style['name']} {{")
            out.append(f"  font-family: var(--font-{family});")
            out.append(f"  font-size: {style['fontSize']};")
            out.append(f"  line-height: {style['lineHeight']};")
            out.append(f"  font-weight: {style['fontWeight']};")
            if "letterSpacing" in style:
                out.append(f"  letter-spacing: {style['letterSpacing']};")
                out.append("  text-transform: uppercase;")
            out += ["}", ""]

    (HERE / "tokens.css").write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {HERE / 'tokens.css'}")


if __name__ == "__main__":
    main()
