from playwright.sync_api import sync_playwright

with sync_playwright() as p :
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://en.wikipedia.org/wiki/Cat')
    print(page.title())
    page.wait_for_timeout(3000)
    print("Chrome Borwser executed successfully")
    browser.close()