import { modifier } from "ember-modifier";
import { DOTS, FRAMES } from "../lib/mascot-frames";

const NOD_AFTER_MS = 450;
const NOD_FOR_MS = 220;
const WINK_FOR_MS = 900;
const MOVE_EVERY_MS = 20000;
const LOOK_AFTER_HOP_MS = 1500;
// keep in sync with the walk and hop animations in common.scss
const MOVES = {
  header: { name: "hop", ms: 2340 },
  "welcome-banner": { name: "walk", ms: 3200 },
};

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

  const move = MOVES[location];
  const looking = () => document.activeElement === input || !!input?.value;
  // a short routine now and then, so it never reads as a static icon
  const routine = () => {
    if (looking()) {
      return;
    }
    set(move.name, true);
    later(() => {
      set(move.name, false);
      if (move.name === "hop" && !looking()) {
        set("look", true);
        later(() => set("look", looking()), LOOK_AFTER_HOP_MS);
      }
    }, move.ms);
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

  input?.addEventListener("focus", onFocus);
  input?.addEventListener("blur", onBlur);
  input?.addEventListener("input", onInput);
  if (menu) {
    observer.observe(menu, { attributes: true, attributeFilter: ["class"] });
  }
  routine();
  const every = setInterval(routine, MOVE_EVERY_MS);

  return () => {
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
  <span class="nautas-mascot" aria-hidden="true" hidden {{watchSearch}}>
    <svg
      class="nautas-mascot__art"
      viewBox="0 0 48 48"
      shape-rendering="crispEdges"
      focusable="false"
    >
      {{#each FRAMES as |frame|}}
        <g class="nautas-mascot__frame nautas-mascot__frame--{{frame.name}}">
          {{#each frame.paths as |shape|}}
            <path fill={{shape.fill}} d={{shape.d}} />
          {{/each}}
        </g>
      {{/each}}
      {{#each DOTS as |x|}}
        <rect class="nautas-mascot__dot" x={{x}} y="1" width="2" height="2" />
      {{/each}}
    </svg>
  </span>
</template>;

export default NautasMascot;
