"""anonist at 48x48: pixel grids composed from parts, one grid per frame.

The drawing's source. Run `python3 docs/frames.py` from the repo root to regenerate
javascripts/discourse/lib/mascot-frames.js, docs/anonist-sprite.svg and docs/frames.png
(the sheet needs Pillow).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SIZE = 48
PALETTE = {
    "#": "#14110F",  # outline
    "@": "#E8E6E1",  # mask
    "o": "#C9C4BB",  # mask shade
    "r": "#D9A49B",  # cheeks
    "h": "#3B3631",  # hood
    "k": "#2A2622",  # hood shade
    "s": "#14110F",  # shoes
}
# colors the theme recolors (the fills above stay as the fallback for the sprite and sheet)
CLASSES = {"h": "nautas-mascot__hood", "k": "nautas-mascot__hood-shade"}

# left half of the mask (12 cols); mirrored to 24
MASK_HALF = [
    "......######",
    "....##@@@@@@",
    "...#@@@@@@@@",
    "..#@@@@@@@@@",
    ".#@@@@@@@@@@",
    ".#@@@@@@@@@@",
    "#@@@@@@@@@@@",
    "#@@#####@@@@",
    "#@#@@@@@#@@@",
    "#@@@@@@@@@@@",
    "#@@@@@@@@@@@",
    "#@@@@@@@@@@@",
    "#@@@@@@@@@@#",
    "#@@@@@@@@@@#",
    "#@rr@@@@@@@#",
    "#@rr@@@@@###",
    "#@@@@@@@@@@@",
    "#@#@@@@@@@@@",
    "#@@#@@@#####",
    ".#@@########",
    ".#@@@####@@@",
    ".#@@@@@@@@@#",
    "..#@@@@@@@@#",
    "..#@@@@@@@@#",
    "...#@@@@@@@#",
    "....#@@@@@@#",
    ".....#@@@@@@",
    "......#@@@@@",
    ".......#@@@@",
    "........####",
]

# eyes: rows 10-11 of the mask, cols 0-23 (None keeps the face)
EYES = {
    "open": ["....@@###@@@@@@@###@@...", "....@#####@@@@#####@...."],
    "shut": ["....@@@@@@@@@@@@@@@@@...", "....@#####@@@@#####@...."],
    "look": ["....@@###@@@@@@@###@@...", "....@@@###@@@@@@###@...."],
    "up": ["....@@###@@@@@@@###@@...", "....@@@@@@@@@@@@@@@@...."],
    "wink": ["....@@###@@@@@@@@@@@@...", "....@#####@@@@#####@...."],
}


def mask(eyes):
    rows = [half + half[::-1] for half in MASK_HALF]
    rows = [list(r) for r in rows]
    for i, line in enumerate(EYES[eyes]):
        for x, ch in enumerate(line):
            if ch != ".":
                rows[10 + i][x] = ch
    # shade the right edge
    for r in rows:
        for x in range(len(r) - 1, 0, -1):
            if r[x] == "#" and r[x - 1] == "@":
                r[x - 1] = "o"
                break
    return ["".join(r) for r in rows]


def blank():
    return [["."] * SIZE for _ in range(SIZE)]


def put(grid, art, x0, y0):
    for y, line in enumerate(art):
        for x, ch in enumerate(line):
            if ch != "." and 0 <= y0 + y < SIZE and 0 <= x0 + x < SIZE:
                grid[y0 + y][x0 + x] = ch


def ellipse(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def hood(grid, dy):
    inside = ellipse(23.5, 15 + dy, 15.2, 14.6)
    for y in range(SIZE):
        for x in range(SIZE):
            if inside(x, y) and y <= 26 + dy:
                edge = not all(
                    inside(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))
                )
                grid[y][x] = "#" if edge else ("k" if x > 30 else "h")


def body(grid, dy):
    # torso: rows 29-39, slightly wider at the bottom
    for y in range(28 + dy, 41):
        half = 8 + (y - 28 - dy) // 6
        for x in range(24 - half - 1, 24 + half + 1):
            edge = x in (24 - half - 1, 24 + half) or y == 40
            grid[y][x] = "#" if edge else ("k" if x > 27 else "h")
    # pocket
    for x in range(19, 29):
        grid[37][x] = "#"


LEGS = {
    # (left leg x, length), (right leg x, length); feet at the bottom
    "stand": ((18, 5), (25, 5)),
    "step-a": ((17, 5), (26, 4)),
    "step-b": ((19, 4), (24, 5)),
    "crouch": ((17, 3), (26, 3)),
    "air": ((19, 3), (24, 3)),
    # sitting on a ledge at row 41: legs hang over it, a little apart
    "dangle": ((16, 6), (27, 6)),
}


def legs(grid, kind):
    for x0, length in LEGS[kind]:
        top = 41
        for y in range(top, top + length):
            for x in range(x0, x0 + 5):
                edge = x in (x0, x0 + 4)
                grid[y][x] = "#" if edge else "k"
        foot = top + length
        for x in range(x0 - 1, x0 + 6):
            if foot < SIZE:
                grid[foot][x] = "s"


def salute(grid, dy):
    """His right arm (the viewer's left) up from the shoulder, hand flat over the brow."""
    for y in range(9 + dy, 33):
        for x in range(8, 13):
            grid[y][x] = "#" if x in (8, 12) else "h"
    for y in range(7 + dy, 11 + dy):
        for x in range(8, 21):
            grid[y][x] = "#" if y in (7 + dy, 10 + dy) or x in (8, 20) else "h"
    # shoulder, joining the arm to the torso
    for y in range(28 + dy, 33):
        for x in range(12, 17):
            grid[y][x] = "#" if y == 32 else "h"


def scratch(grid, dy, shift):
    """His right arm up the side of the hood, hand over the top; shift reaches further to scratch."""
    for y in range(6 + dy, 33):
        for x in range(4, 9):
            grid[y][x] = "#" if x in (4, 8) else "h"
    for y in range(dy, 5 + dy):
        for x in range(4, 21 + shift):
            grid[y][x] = "#" if y in (dy, 4 + dy) or x in (4, 20 + shift) else "h"
    for y in range(28 + dy, 33):
        for x in range(8, 17):
            grid[y][x] = "#" if y == 32 else "h"


FRAMES = {
    "idle": dict(eyes="open", legs="stand"),
    "breathe": dict(eyes="open", legs="stand", dy=1),
    "blink": dict(eyes="shut", legs="stand"),
    "look": dict(eyes="look", legs="stand"),
    "think": dict(eyes="up", legs="stand"),
    "wink": dict(eyes="wink", legs="stand"),
    "walk-a": dict(eyes="open", legs="step-a"),
    "walk-b": dict(eyes="open", legs="step-b", dy=1),
    "crouch": dict(eyes="shut", legs="crouch", dy=2),
    "air": dict(eyes="open", legs="air"),
    "salute": dict(eyes="wink", legs="stand", arm=True),
    "sit": dict(eyes="open", legs="dangle"),
    "sit-blink": dict(eyes="shut", legs="dangle"),
    "scratch-a": dict(eyes="up", legs="dangle", scratch=0),
    "scratch-b": dict(eyes="up", legs="dangle", scratch=4),
}


def frame(eyes, legs_kind, dy=0, arm=False, scratch_shift=None):
    g = blank()
    legs(g, legs_kind)
    body(g, dy)
    hood(g, dy)
    put(g, mask(eyes), 12, 2 + dy)
    if arm:
        salute(g, dy)
    if scratch_shift is not None:
        scratch(g, dy, scratch_shift)
    return g


def grids():
    return {
        name: frame(f["eyes"], f["legs"], f.get("dy", 0), f.get("arm", False), f.get("scratch"))
        for name, f in FRAMES.items()
    }


def sheet(path, scale=8):
    from PIL import Image, ImageDraw

    gs = grids()
    pad = 16
    w = len(gs) * (SIZE * scale + pad) + pad
    h = 2 * (SIZE * scale + pad) + pad + 40
    im = Image.new("RGB", (w, h), "#E8E6E1")
    d = ImageDraw.Draw(im)
    for row, bg in enumerate(("#14110F", "#FFFFFF")):
        for i, (name, g) in enumerate(gs.items()):
            ox = pad + i * (SIZE * scale + pad)
            oy = pad + row * (SIZE * scale + pad + 20)
            d.rectangle([ox, oy, ox + SIZE * scale - 1, oy + SIZE * scale - 1], fill=bg)
            for y, line in enumerate(g):
                for x, ch in enumerate(line):
                    if ch != ".":
                        d.rectangle(
                            [ox + x * scale, oy + y * scale, ox + (x + 1) * scale - 1, oy + (y + 1) * scale - 1],
                            fill=PALETTE[ch],
                        )
            if row == 1:
                d.text((ox, oy + SIZE * scale + 4), name, fill="#14110F")
    im.save(path)





# x of the three thinking dots (2x2 px each, top right)
DOTS = [40, 43, 46]


def paths(grid):
    """One path per color, as row runs: M x y h w v 1 h -w z."""
    runs = {}
    for y, line in enumerate(grid):
        x = 0
        while x < SIZE:
            ch = line[x]
            end = x
            while end < SIZE and line[end] == ch:
                end += 1
            if ch != ".":
                runs.setdefault(ch, []).append(f"M{x} {y}h{end - x}v1h-{end - x}z")
            x = end
    return [(PALETTE[ch], "".join(d), CLASSES.get(ch)) for ch, d in runs.items()]


def write_js(path):
    out = [
        "// Pixel frames drawn on a 48×48 grid; generated by docs/frames.py, do not edit by hand.",
        "export const FRAMES = [",
    ]
    for name, grid in grids().items():
        out.append(f'  {{\n    name: "{name}",\n    paths: [')
        for fill, d, cls in paths(grid):
            cls_line = f'\n        class: "{cls}",' if cls else ""
            out.append(f'      {{\n        fill: "{fill}",{cls_line}\n        d: "{d}",\n      }},')
        out.append("    ],\n  },")
    out.append("];\n")
    out.append(f"export const DOTS = {DOTS};")
    path.write_text("\n".join(out) + "\n")


def write_sprite(path):
    symbols = []
    for name, grid in grids().items():
        body = "".join(f'<path fill="{fill}" d="{d}"/>' for fill, d, _ in paths(grid))
        symbols.append(
            f'<symbol id="anonist-48-{name}" viewBox="0 0 48 48" shape-rendering="crispEdges">{body}</symbol>'
        )
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + "\n".join(symbols) + "\n</svg>\n"
    )


if __name__ == "__main__":
    write_js(ROOT / "javascripts/discourse/lib/mascot-frames.js")
    write_sprite(ROOT / "docs/anonist-sprite.svg")
    sheet(ROOT / "docs/frames.png")
