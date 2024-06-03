# Recreating the previous functions but as actual testes in the CLI
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


# Tester Funcitons from here

def tester01(page:Page):
    '''
    Tester Fucntion to check the title of the page. 
    '''
    page.goto("https://en.wikipedia.org/wiki/Cat")
    
    # Expect title to be Cat - Wikipedia
    expect(page).to_have_title("Cat - Wikipedia")

      
def tester02(page:Page):
    '''
    Tester Fucntion to check the Heading of the page. 
    '''
    page.goto("https://en.wikipedia.org/wiki/Cat")
    expect(page.locator('#firstHeading')).to_have_text('Cat')

def tester03(page:Page):
    '''
    Tester function to check the search bar and search resultant page
    '''
    page.goto('https://en.wikipedia.org/wiki/Cat')
    page.get_by_placeholder('Search Wikipedia').fill("snow leopard")
    page.get_by_role('button', name='Search').click()
    expect(page.locator('#firstHeading')).to_have_text('Snow leopard')
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    pytest.main()