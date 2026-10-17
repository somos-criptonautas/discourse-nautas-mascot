import { click, visit } from "@ember/test-helpers";
import { test } from "qunit";
import { acceptance } from "discourse/tests/helpers/qunit-helpers";

// Theme CSS is not loaded in QUnit, so assert the `hidden` attribute, not visibility.
// The header search field only appears once the welcome banner scrolls away, so use the banner one.
acceptance("Nautas Mascot", function () {
  test("shows the mascot in the welcome banner search", async function (assert) {
    await visit("/");
    assert
      .dom(".search-input--welcome-banner .nautas-mascot")
      .doesNotHaveAttribute("hidden");
    assert.dom(".search-input--welcome-banner.nautas-mascot-host").exists();
    assert
      .dom(".search-input--welcome-banner .nautas-mascot")
      .hasClass("nautas-mascot--walk", "walks in place when it appears");
  });

  test("salutes when clicked", async function (assert) {
    await visit("/");
    await click(".search-input--welcome-banner .nautas-mascot__art");
    assert
      .dom(".search-input--welcome-banner .nautas-mascot")
      .hasClass("nautas-mascot--salute")
      .doesNotHaveClass("nautas-mascot--walk", "the salute stops the walk");
  });

  test("stays hidden where the setting leaves it out", async function (assert) {
    settings.search_locations = "header";
    await visit("/");
    assert
      .dom(".search-input--welcome-banner .nautas-mascot")
      .hasAttribute("hidden");
    assert
      .dom(".search-input--welcome-banner.nautas-mascot-host")
      .doesNotExist();
    settings.search_locations = "header|welcome-banner";
  });
});
