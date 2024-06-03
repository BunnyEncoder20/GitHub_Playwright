import pytest
from playwright.sync_api import sync_playwright, Page, expect

@pytest.fixture(scope="session")
def playwright_setup():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_setup):
    browser = playwright_setup.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

# Tester Functions 
def test01(page:Page):
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    expect(page.locator('#loginh1')).to_have_text('Cookie Controlled Admin')

def test02(page:Page):
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    page.wait_for_selector('//input[@name="username"]').fill('Admin')
    page.wait_for_selector('//input[@name="password"]').fill('AdminPass')
    page.wait_for_selector('//button[@id="login"]').click()
    expect(page.locator('#adminh1')).to_have_text('Admin View')
    

def test03(page:Page):
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    page.wait_for_selector('//input[@name="username"]').fill('Admin')
    page.wait_for_selector('//input[@name="password"]').fill('AdminPass')
    page.wait_for_selector('//button[@id="login"]').click()
    
    page.get_by_text("Go To Login").click()
    expect(page.locator('#adminh1')).to_have_text('Admin View')
    

if __name__ == "__main__":
    pytest.main()