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

- Frames are pixel art on a 32×32 grid. Never edit `mascot-frames.js` by hand; regenerate it from the drawing.
- Motion is in steps only (`steps(1, end)`), never eased tweens, and nothing flashes. Keep the `prefers-reduced-motion` block in sync with any new animation.
- State is classes on the `.nautas-mascot` element (`--look`, `--nod`, `--think`, `--wink`), set from DOM events. The search menu marks a running search with `.loading` on `.search-menu-container`; that is the only signal read from core.
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
- To run CI locally: the `discourse/discourse_test:slim-browsers` image (what [dv](https://github.com/discourse/dv) builds on) with the steps of `discourse/.github`'s `discourse-theme.yml`; set `CI=1` so Chrome starts with `--no-sandbox`.
