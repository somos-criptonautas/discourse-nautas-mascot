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
    "i": "#B5AFA4",  # inside of the mask
    "t": "#3B3631",  # strap
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
    # smiling: both eyes closed upward, as arches
    "happy": ["....@@###@@@@@@###@@@...", "....@#@@@#@@@@#@@@#@...."],
    # following the cursor: the whole eye 1 px to a side
    "left": ["....@###@@@@@@@###@@@...", "....#####@@@@#####@@...."],
    "right": ["....@@@###@@@@@@@###@...", "....@@#####@@@@#####...."],
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
    "smile": dict(eyes="happy", legs="stand"),
    "eyes-left": dict(eyes="left", legs="stand"),
    "eyes-right": dict(eyes="right", legs="stand"),
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


# The floating mask: the same face scaled to 32x40, with a 1 px outline again, plus the
# turn, profile and strapped back of its spin. Rows 41-47 stay free for the bob and shadow.
MASK_W, MASK_H = 32, 40


def scaled(art, w, h):
    """Nearest-neighbour scale; outline pixels (#) on the silhouette are redrawn 1 px thin."""
    src_h, src_w = len(art), len(art[0])
    out = [[art[y * src_h // h][x * src_w // w] for x in range(w)] for y in range(h)]
    inside = lambda x, y: 0 <= x < w and 0 <= y < h and out[y][x] != "."
    edge = lambda x, y: not all(inside(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    for y in range(h):
        for x in range(w):
            if inside(x, y) and edge(x, y):
                out[y][x] = "#"
            elif out[y][x] == "#" and outline_src(art, x * src_w // w, y * src_h // h):
                out[y][x] = "@"
    return ["".join(r) for r in out]


def outline_src(art, x, y):
    """True for a pixel of the source silhouette's outline (not a brow, mouth or other feature)."""
    at = lambda a, b: art[b][a] if 0 <= b < len(art) and 0 <= a < len(art[0]) else "."
    return any(at(x + a, y + b) == "." for a in (-1, 0, 1) for b in (-1, 0, 1))


def silhouette(rows):
    h, w = len(rows), len(rows[0])
    return lambda x, y: 0 <= x < w and 0 <= y < h and rows[y][x] != "."


def near_edge(inside, x, y, d):
    return any(not inside(x + a, y + b) for a in range(-d, d + 1) for b in range(-d, d + 1))


def curved(rows):
    """The front with a shade inside its outline, wider on the right, so it reads as curved."""
    inside = silhouette(rows)
    w = len(rows[0])
    out = [list(r) for r in rows]
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == "@" and near_edge(inside, x, y, 3 if x > w * 2 // 3 else 2):
                out[y][x] = "o"
    return ["".join(r) for r in out]


def back():
    """The mask from behind: a rim of its inside around a dark hollow, as if someone wore it."""
    rows = scaled(mask("open"), MASK_W, MASK_H)
    inside = silhouette(rows)
    out = []
    for y, r in enumerate(rows):
        line = ""
        for x, ch in enumerate(r):
            if ch == ".":
                line += "."
            elif near_edge(inside, x, y, 1):
                line += "#"
            elif near_edge(inside, x, y, 3):
                line += "i"
            else:
                line += "k" if x > MASK_W * 2 // 3 else "h"
        out.append(line)
    return out


def rim():
    """The mask's silhouette in its edge shade: the thickness that shows when it turns."""
    return ["".join(ch if ch in ".#" else "o" for ch in r) for r in back()]


def squeeze(art, w):
    """The mask turned: narrower, keeping its height."""
    return scaled(art, w, len(art))


def strap(grid, x0, x1, y):
    """A strap 3 px high (outline, strap, outline) from x0 to x1, from row y."""
    for x in range(x0, x1):
        for dy in range(3):
            grid[y + dy][x] = "t" if dy == 1 else "#"


# the profile's relief, facing right: (first row, last row, px out) for brow, nose and chin
RELIEF = [(11, 13, 1), (19, 24, 2), (33, 38, 1)]


def profile(grid, top):
    for y0, y1, out in RELIEF:
        for y in range(top + y0, top + y1 + 1):
            edge = max(x for x in range(SIZE) if grid[y][x] != ".")
            grid[y][edge] = "o"
            for x in range(edge + 1, edge + out + 1):
                grid[y][x] = "#" if x == edge + out or y in (top + y0, top + y1) else "@"


def mirrored(grid):
    return [r[::-1] for r in grid]


def float_frame(kind, eyes="open"):
    g = blank()
    x0 = (SIZE - MASK_W) // 2
    front = curved(scaled(mask(eyes), MASK_W, MASK_H))
    if kind == "front":
        put(g, front, x0, 1)
    elif kind in ("turn-a", "turn-b"):
        strap(g, 3, 12, 14)
        put(g, squeeze(rim(), 22), 11, 1)
        put(g, squeeze(front, 22), 15, 1)
        if kind == "turn-b":
            g = mirrored(g)
    elif kind == "side":
        strap(g, 6, 21, 14)
        put(g, squeeze(rim(), 8), 20, 1)
        profile(g, 1)
    elif kind == "back":
        put(g, back(), x0, 1)
        strap(g, 4, 44, 14)
    return g


MASK_FRAMES = {
    "idle": dict(kind="front"),
    "blink": dict(kind="front", eyes="shut"),
    "look": dict(kind="front", eyes="look"),
    "think": dict(kind="front", eyes="up"),
    "wink": dict(kind="front", eyes="wink"),
    "smile": dict(kind="front", eyes="happy"),
    "eyes-left": dict(kind="front", eyes="left"),
    "eyes-right": dict(kind="front", eyes="right"),
    "turn-a": dict(kind="turn-a"),
    "side": dict(kind="side"),
    "back": dict(kind="back"),
    "turn-b": dict(kind="turn-b"),
}


def mask_grids():
    return {name: float_frame(**f) for name, f in MASK_FRAMES.items()}


def grids():
    return {
        name: frame(f["eyes"], f["legs"], f.get("dy", 0), f.get("arm", False), f.get("scratch"))
        for name, f in FRAMES.items()
    }


def all_grids():
    """Both styles, the mask's frames prefixed with mask-: the sheet and the sprite show them all."""
    return {**grids(), **{f"mask-{name}": g for name, g in mask_grids().items()}}


def sheet(path, scale=8):
    from PIL import Image, ImageDraw

    gs = all_grids()
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
# the mask's sparkles while it floats around: 3x3 crosses, at their top-left corners
SPARKS = [(2, 8), (43, 20), (4, 33)]


def spark(x, y):
    return f"M{x + 1} {y}h1v3h-1zM{x} {y + 1}h3v1h-3z"


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


def js_frames(const, gs):
    out = [f"export const {const} = ["]
    for name, grid in gs.items():
        out.append(f'  {{\n    name: "{name}",\n    paths: [')
        for fill, d, cls in paths(grid):
            cls_line = f'\n        class: "{cls}",' if cls else ""
            out.append(f'      {{\n        fill: "{fill}",{cls_line}\n        d: "{d}",\n      }},')
        out.append("    ],\n  },")
    out.append("];\n")
    return out


def write_js(path):
    out = ["// Pixel frames drawn on a 48×48 grid; generated by docs/frames.py, do not edit by hand."]
    out += js_frames("FRAMES", grids())
    out += js_frames("MASK_FRAMES", mask_grids())
    out.append(f"export const DOTS = {DOTS};\n")
    out.append("export const SPARKS = [")
    out += [f'  "{spark(x, y)}",' for x, y in SPARKS]
    out.append("];")
    path.write_text("\n".join(out) + "\n")


def write_sprite(path):
    symbols = []
    for name, grid in all_grids().items():
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
