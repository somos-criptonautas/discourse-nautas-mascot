# Nautas Mascot — agent guide

Rules for anyone changing this repo, people and AI agents alike. Org-wide conventions (README, licenses, commits) are in the [contributing guide](https://github.com/somos-criptonautas/.github/blob/main/CONTRIBUTING.md).

## Scope

A Discourse **theme component**. It renders into the core outlet `search-menu-before-term-input`, so it works on Horizon and on core themes.

```
javascripts/discourse/lib/mascot-frames.js     ← generated pixel frames
javascripts/discourse/components/nautas-mascot.gjs
javascripts/discourse/api-initializers/nautas-mascot.js
common/common.scss                             ← states and step animations
settings.yml, locales/                         ← settings and their descriptions
docs/                                          ← frame sheet and sprite (art source)
```

## Rules

- Frames are pixel art on a 48×48 grid, drawn in `docs/frames.py`. Never edit `mascot-frames.js`, the sprite or `frames.png` by hand; run `python3 docs/frames.py` (the sheet needs Pillow).
- Motion is in steps only (`steps(1, end)`), never eased tweens, and nothing flashes. Keep the `prefers-reduced-motion` block in sync with any new animation.
- State is classes on the `.nautas-mascot` element (`--look`, `--nod`, `--think`, `--wink`, the `--walk`/`--hop` routines and the `--salute` easter egg on click), set from DOM events. The search menu marks a running search with `.loading` on `.search-menu-container`; that is the only signal read from core.
- The mascot is decorative: `aria-hidden`, no text of its own.
- BEM class names, `--d-*`/core color variables over hardcoded colors (the mask colors are the brand's and stay fixed).
- Templates use `{{}}` only; no `innerHTML`.

## Checks

`pnpm install && pnpm lint` runs Discourse's eslint, prettier, stylelint and type checks. CI (`.github/workflows/discourse-theme.yml`) runs lint, the QUnit test in `test/` and core's "core features" spec.

Screenshots in `docs/screenshots/` come from `spec/system/screenshots_spec.rb` via Actions → Screenshots; regular CI skips that spec.

Add conventions and gotchas you discover to this file, in the same PR.

## Gotchas

- In `.gjs` templates a block param named like an HTML/SVG tag turns that tag into a component call: `{{#each paths as |path|}}<path />` crashes the whole search menu. Never name block params after tags.
- QUnit does not load theme CSS, so `isVisible()` is meaningless there; assert the `hidden` attribute instead. On `/` only the welcome-banner search exists; the header field appears once the banner scrolls away.
- System specs run with `Capybara.disable_animation`, so any frame shown only by a keyframe disappears in screenshots; the idle frame keeps `opacity: 1` at rest. On Horizon's `/` the search is the welcome-banner one.
- anonist stands outside the field: on the top border in the welcome banner; right of it in the header, mirrored to face the field, over a floor drawn by the host's `::after` (the mascot itself moves). Horizon's header is 52 px, which fits the 48 px figure plus its 4 px hop; check it there after any size change.
- The hoodie pixels carry `nautas-mascot__hood`/`__hood-shade` classes (from `CLASSES` in `docs/frames.py`); CSS recolors them with `--primary-medium`, the `fill` is only the sprite's fallback.
- The salute click is stopped from propagating, so it doesn't open the search menu; it stays an easter egg (no pointer cursor, still `aria-hidden`).
- Walk and hop durations live in both `common.scss` (`$walk-step`, `$hop-step`) and `MOVES` in the component; change them together.
- `sit`, `sit-blink` and `scratch-a`/`-b` are drawn for the community-sidebar mascot of `somos-criptonautas/ghost-headline-theme-nautas`, which copies `docs/anonist-sprite.svg` to its `assets/images/`; this component doesn't show them. Copy the sprite there again after changing frames.
- To run CI locally: the `discourse/discourse_test:slim-browsers` image (what [dv](https://github.com/discourse/dv) builds on) with the steps of `discourse/.github`'s `discourse-theme.yml`; set `CI=1` so Chrome starts with `--no-sandbox`.
