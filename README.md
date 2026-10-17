# Nautas Mascot

**ENGLISH** | [ESPAÑOL](README.es.md)

Maintained by Criptonautas. Not affiliated with or endorsed by Discourse (Civilized Discourse Construction Kit, Inc.).

A Discourse theme component that puts **anonist**, the community mascot, in the search field. It invites a question rather than a keyword.

| Idle | Search field in focus |
|---|---|
| ![anonist in the header search](docs/screenshots/mascot-header.png) | ![anonist looking at the field](docs/screenshots/mascot-header-focus.png) |

## What it does

anonist takes the magnifier's place and moves in steps, 8-bit style:

| When | Frame |
|---|---|
| Nothing happens | breathes (up one pixel) and blinks now and then |
| The field gets focus | looks at what you type |
| You pause while typing | nods one pixel |
| The search is running | thinks, with three dots lighting up |
| Results arrive | winks |

With *reduce motion* turned on in the system, it stays still and only changes frame on state changes.

## Settings

| Setting | Default | What it does |
|---|---|---|
| `search_locations` | `header`, `welcome-banner` | Search fields that show the mascot |
| `mascot_size` | `32` | Size in pixels; 32 is the drawing's own size |

## Install

**Admin → Appearance → Themes → Install → From a git repository**, with this repo's URL. Then add it as a component of your main theme. [How to install a theme component](https://meta.discourse.org/t/how-do-i-install-a-theme-or-theme-component/63682)

## Files

| Path | Contents |
|---|---|
| `javascripts/discourse/lib/mascot-frames.js` | The six frames as pixel paths (generated, do not edit by hand) |
| `javascripts/discourse/components/nautas-mascot.gjs` | Renders the frames and reads focus, typing and search state |
| `common/common.scss` | Which frame shows in each state, and the step animations |
| `docs/` | Frame sheet and SVG sprite, the drawing's source |

## License

Code: [MIT](LICENSE). The anonist drawing (the frames and `docs/`): [CC BY-NC-SA 4.0](CC-BY-NC-SA-4.0.txt), like the rest of the Criptonautas brand materials.
