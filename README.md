# GitHub_Playwright

- This is a Repo to record my technical learning for my Internship at L&T
- In this repo I'll be learning and trying to automate the testing of website (starting with a login page)
- We will be using Playwright with Python to make the testing scripts
- Website for testing, automations scenarios : [Automation Practice Website]('https://testpages.eviltester.com/styled/index.html)

---

## 1. Launching Chrome 

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p :
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page()
    page.goto('https://en.wikipedia.org/wiki/Cat')
    print(page.title())
    page.wait_for_timeout(3000)
    print("Chrome Borwser executed successfully")
    browser.close()
```
- `sync_playwright` imports the sync_playwright module from the Playwright library, which is used to control browsers programmatically.
- Within the `with` block, `sync_playwright` can be accessed as `p`
- `p.chrominum.launch(headless=False)` launches the chromium browser with headless=Flase (so that we cna see the browser actions on screen. By default this is set to True and all the actios happen in the backend). This browser instance is then assigned to the "browser" variable.
- Using it, we can open pages and tabs in the browser window. 
- `page = browser.new_page()` opens a new tab in the fresh browser window. 
- `page.goto('...url...')` navigates to a given url
- `page.title()` fetches the page title
- `page.wait_for_timeout(3000)` makes the page wait for 3000 ms (3 seconds)
- `browser.close()` closed the browser window, ending the session.

---

## 2 Locators

- Using the **inspect page** option, we can select the element we want to target and get it's attribute and properties. 
- There are several ways in which we can loacte an element on the web page using Playwright:

1. `page.get_by_role()` : When locating by role, you should usually pass the accessible name as well, so that the locator pinpoints the exact element.
Eg:
![alt text](/notes%20images/image01.png)
```python
expect(page.get_by_role("heading", name="Sign up")).to_be_visible()

page.get_by_role("checkbox", name="Subscribe").check()

page.get_by_role("button", name=re.compile("submit", re.IGNORECASE)).click()
```
<br>

2. `page.get_by_label("label")` 
Eg:
```python
page.get_by_label("Password").fill("secret")
```
<br>

3. `page.get_by_placeholder()` usually used for input form type. We can locate and fill these using the `.fill()` function.
Eg:
```python
page.get_by_placeholder("name@example.com").fill("playwright@microsoft.com")
```

4. `page.get_by_text()` finds the element by the text it contains. Can be a sub string, exact match or regular expression.
Eg:
```python
expect(page.get_by_text("Welcome, John")).to_be_visible()
expect(page.get_by_text("Welcome, John", exact=True)).to_be_visible()
expect(page.get_by_text(re.compile("welcome, john", re.IGNORECASE))).to_be_visible()
```
<br>

5. `page.get_by_alt_text()` is used for locating images tags. We can click on the image after locating it using the `click()` method.
Eg:
```python
page.get_by_alt_text("playwright logo").click()
```
<br>

6. `page.get_by_title()` used when we want an element with a specific title attribute
Eg:
```python
expect(page.get_by_title("Issues count")).to_have_text("25 issues")
```
<br>

7. `page.wait_for_selector()` can be used to get the elements by their attributes like #id or .class (avoid using classes).
Eg:
```python 
page_title = page.wait_for_selector('#firstHeading')
```
<br>


---

## 3 Testcase Functions 

- When making the testcase functions, we need to add some decoraters on the top, which will help in showing which test cases are padding and which are failing in the commmand line. 
- Below are basic decorators for isoloation testing :

```python
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
```

### Explaination

- `@pytest.fixture(scope='session')` : This decorator defines a fixture that has a session scope, meaning it is created once per test session and shared among all tests.

<br>

- The **playwright_setup()** fixture initiliatizes playwright. The `yeild` statement makes **playwright** instance available to any tes function which is dependent on the playwright_setup().
- When all the tests are done, the context manager exits, cleaning up the playwright resources.

<br>

- The **browser(playwright_setup)** fixture launches a chrominum browser using playwright. 

<br>

- The **page(browser)** fixture creates a new browser context and a new page (tab) within that context.
- It has function scope (it is created once per test function), ensuring isolation between the tests


---

## Xpath 

- used for traversing between web elements 
```
'//' = realtive xpath
'//tagName[@attributename="attributeValue"]' = selecting any web element using it's attribute
```
- Eg:
```
//input[@name="username"]
```

---

## Simple Login Testing 

- I used a dummy website to login recreate a login page.
- Made a simple script to navigate the login page, login into the site and verify that the user reached the landing page.

```python
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
```
