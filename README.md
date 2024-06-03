# GitHub_Playwright

- This is a Repo to record my technical learning for my Internship at L&T
- In this repo I'll be learning and trying to automate the testing of website (starting with a login page)
- We will be using Playwright with Python to make the testing scripts

## 1. Launching Chrome 

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p :
    browser = p.chrmium.launch(headless=False) 
    page = browser.new_page()
    page.goto('https://en.wikipedia.org/wiki/Cat')
    print(page.title())
    page.wait_for_timeout(3000)
    print("Chrome Borwser executed successfully")
    browser.close()
```