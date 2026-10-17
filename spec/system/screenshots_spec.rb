# frozen_string_literal: true

# README screenshots. Run by the "Screenshots" workflow, which commits the PNGs
# to docs/screenshots/. Skipped in regular CI.
RSpec.describe "Screenshots" do
  before { skip "set SCREENSHOTS=1 to take screenshots" unless ENV["SCREENSHOTS"] }

  let!(:horizon) do
    SystemThemesManager.sync_theme!("horizon")
    theme = Theme.horizon_theme
    theme.update!(enabled: true, user_selectable: true)
    SiteSetting.default_theme_id = theme.id
    theme
  end
  let!(:component) { upload_theme_component(parent_theme_id: horizon.id) }

  def save(name)
    path = Rails.root.join("tmp/capybara/screenshots/#{name}.png")
    FileUtils.mkdir_p(path.dirname)
    page.driver.with_playwright_page do |pw|
      pw.screenshot(path: path.to_s, clip: { x: 0, y: 0, width: 1280, height: 120 })
    end
  end

  it "shows the mascot in the header search" do
    resize_window(width: 1280, height: 900) do
      visit "/"
      expect(page).to have_css(".search-input--header .nautas-mascot")
      save("mascot-header")
      find("#header-search-input").click
      expect(page).to have_css(".nautas-mascot--look")
      save("mascot-header-focus")
    end
  end
end
