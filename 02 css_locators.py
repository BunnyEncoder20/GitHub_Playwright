from playwright.sync_api import sync_playwright, expect

with sync_playwright() as play:
    browser = play.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://en.wikipedia.org/wiki/Cat')

    # cssSelectors : id='#id'
    # page.querySelector() - used to get element with given selector
    # page.wait_for_selector() - used to make the script wait for the selector to appear before looking for it. Better to use this 
    # page.locate_by_role() - recommended way to locate elements on the webpage, because this is usually how users and aserive technologies see the page elements

    page_title = page.wait_for_selector('#firstHeading')
    print(page_title)

    # Selecting elements
    serach_button = page.get_by_role("button", name="Search")

    # actions
    expect(page).to_have_title("Cat - Wikipedia")                       
    page.get_by_placeholder('Search Wikipedia').fill("snow leopard")
    # page.wait_for_timeout(3000)
    serach_button.click()
    expect(page.locator('#firstHeading')).to_have_text('Snow leopard')  

    page.wait_for_timeout(3000)
    browser.close()

