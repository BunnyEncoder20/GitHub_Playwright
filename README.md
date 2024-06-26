# GitHub_Playwright

- This is a Repo to record my technical learning for my Internship at L&T
- In this repo I'll be learning and trying to automate the testing of website (starting with a login page)
- We will be using Playwright with Python to make the testing scripts
- Website for testing, automations scenarios : [Automation Practice Website]('https://testpages.eviltester.com/styled/index.html)

---

## Launching Chrome 

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

## Running Tests

- By default the tests run in headless mode 
- To run the tests in headed mode, we can change the headless parameter to `False`
```python
browser = playwright_setup.chromium.launch(headless=False)
```
- We can also change the browser on which we want to test by modifying the same line of code : 

```python 
browser = playwright_setup.chromium.launch()
browser = playwright_setup.firefox.launch()
browser = playwright_setup.webkit.launch()
```

---

## Locators

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

## Testcase Functions 

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

- I used a [dummy website]('https://testpages.eviltester.com/styled/cookies/adminlogin.html') to login recreate a login page.
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

<br>

- A good login testing would look something like:
    1. Verify the presence and visibility of page elements.
    2. Test with valid registration and login credentials.
    3. Test with invalid and empty details.
    4. Test error handling and displaying of appropriate error messages.
    5. Test "Remember me" functionality.
    6. Test password visibility toggle.
    7. Test login with multi-factor authentication.
    8. Test email confirmation after successful registration.
    9. Test social media signup/login integrations
    10. Test concurrent user sessions.
    11. Test the effect of multiple login failures.
    12. Test how accessible your pages are.
    13. Test the responsiveness of the pages.
    14. Test login behavior with browser autofill.
    15. Test CAPTCHA protections against bot signups.

- For the given website, some tests could include : 

```python
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
```

---

## CodeGen

- **Codegen** is a powerful tool which comes in playwright which is used to generate test script lines directly from user interaction on the website 
welcome@312021
```
playwright codegen urlHere
```
- url is optional and can be entered directly in the browser window itself
- Run `codegen` and perform actions in the browser. 
- The terminal will open 2 windows : 
    - The browser window 
    - The Playwright inspector (which shows the recorded code)
- Playwright will generate the code for the user interactions. 
- `Codegen` will look at the rendered page and figure out the recommended locator, prioritizing role, text and test id locators.
- Assertions by clicking on one of the icons in the toolbar and then clicking on an element on the page to assert against. You can choose:
    - `assert visibility` to assert that an element is visible
    - `assert text` to assert that an element contains specific text
    - `assert value` to assert that an element has a specific value

![alt text](./notes%20images/image02.png)

---

## Actions 

- Playwright can interact with HTML Input elements such as text inputs, checkboxes, radio buttons, select options, mouse clicks, type characters, keys and shortcuts as well as upload files and focus elements.

**1. Text Input**
    - Using locator.fill() is the easiest way to fill out the form fields. It works for \<input\>, \<textarea\> and [contenteditable] elements. 
    - Input fields are best located using the .get_by_label()
    - Eg:
```python
# Text input
page.get_by_role("textbox").fill("Peter")

# Date input
page.get_by_label("Birth date").fill("2020-02-02")

# Time input
page.get_by_label("Appointment time").fill("13:15")

# Local datetime input
page.get_by_label("Local time").fill("2020-03-02T05:15")
```

**2. Checkboxes and radio buttons** 

```python
# Check the checkbox
page.get_by_label('I agree to the terms above').check()

# Assert the checked state
expect(page.get_by_label('Subscribe to newsletter')).to_be_checked()

# Select the radio button
page.get_by_label('XL').check()
```
**3. Select Options**

```python
# Single selection matching the value or label
page.get_by_label('Choose a color').select_option('blue')

# Single selection matching the label
page.get_by_label('Choose a color').select_option(label='Blue')

# Multiple selected items
page.get_by_label('Choose multiple colors').select_option(['red', 'green', 'blue'])
```

**4. Mouse Click**

```python
# Generic click
page.get_by_role("button").click()

# Double click
page.get_by_text("Item").dblclick()

# Right click
page.get_by_text("Item").click(button="right")

# Shift + click
page.get_by_text("Item").click(modifiers=["Shift"])

# Hover over element
page.get_by_text("Item").hover()

# Click the top left corner
page.get_by_text("Item").click(position={ "x": 0, "y": 0})
```

**5. Keyboard Inputs**

```python
# Hit Enter
page.get_by_text("Submit").press("Enter")

# Dispatch Control+Right
page.get_by_role("textbox").press("Control+ArrowRight")

# Press $ sign on keyboard
page.get_by_role("textbox").press("$")
```
- Other keyboard keys available : 
```
Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape,
ArrowDown, End, Enter, Home, Insert, PageDown, PageUp, ArrowRight,
ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc.
```

**6. Uploading files**
- `locator.set_input_files()` method
- can upload multiple files using an array 
- empty array reemoves the selected files 

```python 
# Select one file
page.get_by_label("Upload file").set_input_files('myfile.pdf')

# Select multiple files
page.get_by_label("Upload files").set_input_files(['file1.txt', 'file2.txt'])

# Remove all the selected files
page.get_by_label("Upload file").set_input_files([])
```

**7. Focus on Element**
- locator.focus()

```python
page.get_by_label('password').focus()
```

**8. Drag and Drop**
- This method performs : 
    - Hover the mouse on element that will be dragged 
    - press left mouse down
    - drag the mpuse to element that will recieve the drop
    - release left mouse button

```python
page.locator("#item-to-be-dragged").drag_to(page.locator("#item-to-drop-at"))
```

- If you want precise control over the drag operation, use lower-level methods

```python
page.locator("#item-to-be-dragged").hover()
page.mouse.down()
page.locator("#item-to-drop-at").hover()
page.mouse.up()
```

---

## Assertions 
- Here is a list of some common Assertions 

| Assertion                         | Description                       |
|-----------------------------------|-----------------------------------|
| expect(locator).to_be_checked()   | Checkbox is checked               |
| expect(locator).to_be_disabled()  | Element is disabled               |
| expect(locator).to_be_empty()     | Container is empty                |
| expect(locator).to_be_enabled()   | Element is enabled                |
| expect(locator).to_be_focused()   | Element is focused                |
| expect(locator).to_be_hidden()    | Element is not visible            |
| expect(locator).to_be_visible()   | Element is visible                |
| expect(locator).to_contain_text() | Element contains text             |
| expect(locator).to_have_count()   | List has exact number of children |
| expect(locator).to_have_text()    | Element matches text              |
| expect(locator).to_have_value()   | Input has a value                 |
| expect(locator).to_have_values()  | Select has options selected       |
| expect(page).to_have_title()      | Page has a title                  |
| expect(page).to_have_url()        | Page has a URL                    |
| expect(response).to_be_ok()       | Response has an OK status         |

