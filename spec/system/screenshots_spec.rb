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
      # the field plus the space above it, where anonist stands
      box = pw.locator(".search-input--welcome-banner").bounding_box
      clip = {
        x: box["x"] - 8,
        y: box["y"] - 56,
        width: box["width"] + 16,
        height: box["height"] + 64,
      }
      pw.screenshot(path: path.to_s, clip: clip)
    end
  end

  # Horizon's home page shows the welcome-banner search; the header one appears only after scrolling.
  it "shows the mascot in the search field" do
    resize_window(width: 1280, height: 900) do
      visit "/"
      expect(page).to have_css(".search-input--welcome-banner .nautas-mascot:not([hidden])")
      expect(page).to have_no_css(".nautas-mascot--walk") # animations are off in specs
      save("mascot-search")
      find("#welcome-banner-search-input").click
      expect(page).to have_css(".nautas-mascot--look")
      save("mascot-search-focus")
    end
  end

  it "hides the mascot on tablets, where there's no room for it" do
    resize_window(width: 800, height: 1000) do
      visit "/"
      expect(page).to have_css(".search-input--welcome-banner.nautas-mascot-host")
      expect(page).to have_no_css(".search-input--welcome-banner .nautas-mascot", visible: true)
    end
  end

  it "shows the mask style in the search field" do
    component.update_setting(:mascot_style, "mask")
    component.save!
    resize_window(width: 1280, height: 900) do
      visit "/"
      expect(page).to have_css(".search-input--welcome-banner .nautas-mascot--mask")
      expect(page).to have_no_css(".nautas-mascot--orbit")
      save("mascot-mask-search")
    end
  end
end
