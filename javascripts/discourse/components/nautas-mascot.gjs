import { modifier } from "ember-modifier";
import { DOTS, FRAMES, MASK_FRAMES, SPARKS } from "../lib/mascot-frames";

const NOD_AFTER_MS = 450;
const NOD_FOR_MS = 220;
const WINK_FOR_MS = 900;
const MOVE_EVERY_MS = 20000;
const LOOK_AFTER_MOVE_MS = 1500;
// per mascot_style: the routine for each search field and the easter egg on click;
// keep the durations in sync with the animations in common.scss
const MOVES = {
  figure: {
    header: { name: "hop", ms: 2340 },
    "welcome-banner": { name: "walk", ms: 3200 },
    click: { name: "salute", ms: 1400 },
  },
  mask: {
    header: { name: "drift", ms: 1800 },
    "welcome-banner": { name: "orbit", ms: 3000 },
    click: { name: "spin", ms: 1080 },
  },
};

const framesFor = (style) => (style === "mask" ? MASK_FRAMES : FRAMES);

// State lives in classes on the element, not tracked properties: every change comes from
// DOM events outside Ember's render, and CSS picks the frame.
const watchSearch = modifier((element) => {
  const box = element.closest(".search-input");
  const location = [...(box?.classList ?? [])]
    .find((name) => name.startsWith("search-input--"))
    ?.replace("search-input--", "");

  if (!box || !settings.search_locations.split("|").includes(location)) {
    element.hidden = true;
    return;
  }

  element.hidden = false;
  box.classList.add("nautas-mascot-host");

  const input = box.querySelector("input");
  const menu = element.closest(".search-menu-container");
  const timers = new Set();
  const later = (fn, ms) => {
    const id = setTimeout(() => {
      timers.delete(id);
      fn();
    }, ms);
    timers.add(id);
    return id;
  };
  const set = (name, on) =>
    element.classList.toggle(`nautas-mascot--${name}`, on);

  const moves = MOVES[settings.mascot_style];
  const move = moves[location];
  const egg = moves.click;
  const looking = () => document.activeElement === input || !!input?.value;
  // a short routine now and then, so it never reads as a static icon
  const routine = () => {
    if (looking()) {
      return;
    }
    set(move.name, true);
    later(() => {
      set(move.name, false);
      if (location === "header" && !looking()) {
        set("look", true);
        later(() => set("look", looking()), LOOK_AFTER_MOVE_MS);
      }
    }, move.ms);
  };

  // easter egg: a salute or a spin when clicked; kept off the search menu's own click handling
  const onClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    set(move.name, false);
    set(egg.name, true);
    later(() => set(egg.name, false), egg.ms);
  };

  let pause;
  const onFocus = () => {
    set(move.name, false);
    set("look", true);
  };
  const onBlur = () => set("look", false);
  const onInput = () => {
    clearTimeout(pause);
    pause = later(() => {
      set("nod", true);
      later(() => set("nod", false), NOD_FOR_MS);
    }, NOD_AFTER_MS);
  };

  // eyes toward the cursor; only the pointer's x is read, never kept or sent
  let eyesFrame;
  const onPointer = (event) => {
    cancelAnimationFrame(eyesFrame);
    eyesFrame = requestAnimationFrame(() => {
      const { left, right } = element.getBoundingClientRect();
      let side =
        event.clientX < left ? "left" : event.clientX > right ? "right" : null;
      // the header one is drawn mirrored
      if (side && location === "header") {
        side = side === "left" ? "right" : "left";
      }
      set("eyes-left", side === "left");
      set("eyes-right", side === "right");
    });
  };
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let wasLoading = false;
  const observer = new MutationObserver(() => {
    const loading = menu.classList.contains("loading");
    set("think", loading);
    if (wasLoading && !loading && input?.value) {
      set("wink", true);
      later(() => set("wink", false), WINK_FOR_MS);
    }
    wasLoading = loading;
  });

  element.addEventListener("click", onClick);
  if (!still) {
    document.addEventListener("pointermove", onPointer, { passive: true });
  }
  input?.addEventListener("focus", onFocus);
  input?.addEventListener("blur", onBlur);
  input?.addEventListener("input", onInput);
  if (menu) {
    observer.observe(menu, { attributes: true, attributeFilter: ["class"] });
  }
  routine();
  const every = setInterval(routine, MOVE_EVERY_MS);

  return () => {
    element.removeEventListener("click", onClick);
    document.removeEventListener("pointermove", onPointer);
    cancelAnimationFrame(eyesFrame);
    input?.removeEventListener("focus", onFocus);
    input?.removeEventListener("blur", onBlur);
    input?.removeEventListener("input", onInput);
    observer.disconnect();
    clearInterval(every);
    timers.forEach(clearTimeout);
    box.classList.remove("nautas-mascot-host");
  };
});

const NautasMascot = <template>
  <span
    class="nautas-mascot nautas-mascot--{{settings.mascot_style}}"
    aria-hidden="true"
    hidden
    {{watchSearch}}
  >
    <svg
      class="nautas-mascot__art"
      viewBox="0 0 48 48"
      shape-rendering="crispEdges"
      focusable="false"
    >
      {{! the mask's shadow and sparkles stay put while its frames bob }}
      <rect class="nautas-mascot__shadow" x="14" y="45" width="20" height="2" />
      {{#each SPARKS as |d|}}
        <path class="nautas-mascot__spark" d={{d}} />
      {{/each}}
      <g class="nautas-mascot__float">
        {{#each (framesFor settings.mascot_style) as |frame|}}
          <g class="nautas-mascot__frame nautas-mascot__frame--{{frame.name}}">
            {{#each frame.paths as |shape|}}
              <path class={{shape.class}} fill={{shape.fill}} d={{shape.d}} />
            {{/each}}
          </g>
        {{/each}}
        {{#each DOTS as |x|}}
          <rect class="nautas-mascot__dot" x={{x}} y="1" width="2" height="2" />
        {{/each}}
      </g>
    </svg>
  </span>
</template>;

export default NautasMascot;
