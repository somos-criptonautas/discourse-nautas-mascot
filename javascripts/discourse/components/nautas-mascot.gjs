import { modifier } from "ember-modifier";
import { DOTS, FRAMES } from "../lib/mascot-frames";

const NOD_AFTER_MS = 450;
const NOD_FOR_MS = 220;
const WINK_FOR_MS = 900;

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

  let pause;
  const onFocus = () => set("look", true);
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

  return () => {
    input?.removeEventListener("focus", onFocus);
    input?.removeEventListener("blur", onBlur);
    input?.removeEventListener("input", onInput);
    observer.disconnect();
    timers.forEach(clearTimeout);
    box.classList.remove("nautas-mascot-host");
  };
});

const NautasMascot = <template>
  <span class="nautas-mascot" aria-hidden="true" hidden {{watchSearch}}>
    <svg
      class="nautas-mascot__art"
      viewBox="0 0 32 32"
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
        <rect class="nautas-mascot__dot" x={{x}} y="1" width="1" height="1" />
      {{/each}}
    </svg>
  </span>
</template>;

export default NautasMascot;
