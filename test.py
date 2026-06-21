# Script for testing the basic functionality needed for the project
import os

from playwright.sync_api import sync_playwright

# Get the company portal URL from the .env file
from dotenv import load_dotenv
import time

from utils import apply_input, get_button_by_text, get_element_by_id

load_dotenv()

# Login credentials for the different portals
company_portal_savers_login = os.getenv("COMPANY_PORTAL_SAVERS_LOGIN")
savers_id = os.getenv("SAVERS_ID")
savers_telephone = os.getenv("SAVERS_TELEPHONE")

company_portal_agents_login = os.getenv("COMPANY_PORTAL_AGENTS_LOGIN")
agents_username = os.getenv("AGENTS_USERNAME")
agents_password = os.getenv("AGENTS_PASSWORD")

company_portal_emp_login = os.getenv("COMPANY_PORTAL_EMP_LOGIN")
emp_username = os.getenv("EMP_USERNAME")

# def test_savers_login(context):
#     savers_page = context.new_page()
#     savers_page.goto(company_portal_savers_login)

#     apply_input(savers_page, "idNumber", savers_id)
#     apply_input(savers_page, "phone", savers_telephone)

#     login_button = get_button_by_text(savers_page, "כניסה")

#     start = time.perf_counter()

#     with savers_page.expect_navigation():
#         login_button.click()

#     duration = time.perf_counter() - start

#     print(f"Navigation took {duration:.3f}s")

#     savers_page.wait_for_timeout(5000)  # Wait for 5 seconds

def test_agents_login(context):
    agents_page = context.new_page()
    agents_page.goto(company_portal_agents_login)

    apply_input(agents_page, "UserName", agents_username)
    apply_input(agents_page, "Password", agents_password)

    token_input = get_element_by_id(agents_page, "CodeToken")

    login_button = get_element_by_id(agents_page, "btnLoginSubmit")

    token = input("Enter the 2FA token: ")
    token_input.fill(token)

    start = time.perf_counter()
    with agents_page.expect_navigation():
        login_button.click()
    duration = time.perf_counter() - start

    print(f"Navigation took {duration:.3f}s")

def test_basic_functionality():

    with sync_playwright() as p:
        
        # Launch Chrome browser
        print("Launching browser...")
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context()

        # agents_page = context.new_page()
        # agents_page.goto(company_portal_agents_login)
        # agents_page.wait_for_timeout(5000)  # Wait for 5 seconds


        # emp_page = context.new_page()
        # emp_page.goto(company_portal_emp_login)
        # emp_page.wait_for_timeout(5000)  # Wait for 5 seconds

        test_agents_login(context)

        # Wait for 10 seconds to observe the logged-in state
        time.sleep(10)

        # Close the browser
        print("Closing browser...")
        browser.close()


if __name__ == "__main__":
    test_basic_functionality()