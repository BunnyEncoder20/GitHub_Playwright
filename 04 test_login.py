import pytest
from playwright.sync_api import sync_playwright, Page, expect

@pytest.fixture(scope="session")
def playwright_setup():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_setup):
    browser = playwright_setup.chromium.launch(headless=True)
    # browser = playwright_setup.firefox.launch(headless=False)
    # browser = playwright_setup.webkit.launch(headless=False)
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
    '''
    Visibility Check
    '''
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    expect(page.locator('#loginh1')).to_have_text('Cookie Controlled Admin')
    expect(page.get_by_label('username')).to_be_visible()
    expect(page.get_by_label('password')).to_be_visible()
    expect(page.get_by_role('button',name='Login')).to_be_visible()
    expect(page.get_by_role('checkbox',name='Remember me')).to_be_visible()
    

def test02(page:Page):
    '''
    Valid credentials login
    '''
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    page.wait_for_selector('//input[@name="username"]').fill('Admin')
    page.wait_for_selector('//input[@name="password"]').fill('AdminPass')
    page.wait_for_selector('//button[@id="login"]').click()
    expect(page.locator('#adminh1')).to_have_text('Admin View')
    
def test03(page:Page):
    '''
    Invalid credentials login
    '''
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    page.wait_for_selector('//input[@name="username"]').fill('NotAdmin')
    page.wait_for_selector('//input[@name="password"]').fill('NotAdminPass')
    page.wait_for_selector('//button[@id="login"]').click()
    expect(page.get_by_role('heading',name='Login Details Incorrect')).to_be_visible()

def test04(page:Page):
    '''
    Verify That Login page cannot be accessed once Logged in.
    '''
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    page.wait_for_selector('//input[@name="username"]').fill('Admin')
    page.wait_for_selector('//input[@name="password"]').fill('AdminPass')
    page.wait_for_selector('//button[@id="login"]').click()
    
    page.get_by_text("Go To Login").click()
    expect(page.locator('#adminh1')).to_have_text('Admin View')

def test05(page:Page):
    '''
    Test to see that logout is working and redirecting to crrect page
    '''    
    page.goto('https://testpages.eviltester.com/styled/cookies/adminlogin.html')
    page.wait_for_selector('//input[@name="username"]').fill('Admin')
    page.wait_for_selector('//input[@name="password"]').fill('AdminPass')
    page.wait_for_selector('//button[@id="login"]').click()

    expect(page.locator('#adminh1')).to_have_text('Admin View')
    page.get_by_text('Admin Logout').click()
    
    expect(page.get_by_role('heading',name='Cookie Controlled Admin')).to_be_visible()


if __name__ == "__main__":
    pytest.main()