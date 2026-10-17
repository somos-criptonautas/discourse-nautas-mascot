import { visit } from "@ember/test-helpers";
import { test } from "qunit";
import { acceptance } from "discourse/tests/helpers/qunit-helpers";

acceptance("Nautas Mascot", function (needs) {
  needs.settings({ search_experience: "search_field" });

  test("shows the mascot in the header search", async function (assert) {
    await visit("/");
    assert.dom(".search-input--header .nautas-mascot").isVisible();
    assert.dom(".search-input--header.nautas-mascot-host").exists();
  });

  test("stays hidden where the setting leaves it out", async function (assert) {
    settings.search_locations = "welcome-banner";
    await visit("/");
    assert.dom(".search-input--header .nautas-mascot").isNotVisible();
    settings.search_locations = "header|welcome-banner";
  });
});
