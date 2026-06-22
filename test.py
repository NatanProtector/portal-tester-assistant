# Script for testing the basic functionality needed for the project
import os

from playwright.sync_api import sync_playwright

# Get the company portal URL from the .env file
from dotenv import load_dotenv
import time

from utils import apply_input, get_element_by_id, get_element_by_name, get_element_by_text, get_input_by_id, two_fa_code_is_valid

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

def test_savers_login(context):
    savers_page = context.new_page()
    savers_page.goto(company_portal_savers_login)

    get_element_by_text(savers_page, "סמס ").click()

    apply_input(savers_page, "idNumber", savers_id)
    apply_input(savers_page, "phone", savers_telephone)

    login_button = get_element_by_text(savers_page, " המשך ")

    input("Get you phone ready to receive 2FA code, then press Enter to continue...")

    start = time.perf_counter()
    login_button.click()

    input("Press Enter when you receive the 2FA code...")

    two_fa_duration = time.perf_counter() - start

    two_fa_code = input("Enter the 2FA code: ")

    while not two_fa_code_is_valid(two_fa_code):
        print("Invalid 2FA code, please try again.")
        two_fa_code = input("Enter the 2FA code: ")

    ontimeInput1 = get_input_by_id(savers_page, "ontimeInput1")
    ontimeInput2 = get_input_by_id(savers_page, "ontimeInput2")
    ontimeInput3 = get_input_by_id(savers_page, "ontimeInput3")
    ontimeInput4 = get_input_by_id(savers_page, "ontimeInput4")
    ontimeInput5 = get_input_by_id(savers_page, "ontimeInput5")
    ontimeInput6 = get_input_by_id(savers_page, "ontimeInput6")

    ontimeInput1.fill(two_fa_code[0])
    ontimeInput2.fill(two_fa_code[1])
    ontimeInput3.fill(two_fa_code[2])
    ontimeInput4.fill(two_fa_code[3])
    ontimeInput5.fill(two_fa_code[4])

    start = time.perf_counter()

    with savers_page.expect_navigation():
        ontimeInput6.fill(two_fa_code[5])
        
        duration = time.perf_counter() - start


    return two_fa_duration, duration

def test_agents_login(context):
    agents_page = context.new_page()
    agents_page.goto(company_portal_agents_login)

    apply_input(agents_page, "UserName", agents_username)
    apply_input(agents_page, "Password", agents_password)

    token_input = get_element_by_id(agents_page, "CodeToken")

    login_button = get_element_by_id(agents_page, "btnLoginSubmit")

    token = input("Enter the ComSign token: ")
    token_input.fill(token)

    start = time.perf_counter()
    with agents_page.expect_navigation():
        login_button.click()
    duration = time.perf_counter() - start

    return duration

def test_emp_login(context):
    emp_page = context.new_page()
    emp_page.goto(company_portal_emp_login)

    apply_input(emp_page, "txtUsername", emp_username)

    token_input = get_element_by_id(emp_page, "txtToken")

    login_button = get_element_by_name(emp_page, "btnNext")

    token = input("Enter the ComSign token: ")
    token_input.fill(token)

    start = time.perf_counter()
    with emp_page.expect_navigation():
        login_button.click()
    duration = time.perf_counter() - start

    return duration

def test_basic_functionality():

    with sync_playwright() as p:
        
        # Launch Chrome browser
        print("Launching browser...")
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context()

        savers_duration_2FA, savers_duration_final = test_savers_login(context)

        print(f"Savers login navigation took {savers_duration_2FA:.3f}s for 2FA and {savers_duration_final:.3f}s for final navigation")

        emp_duration = test_emp_login(context)

        print(f"EMP login navigation took {emp_duration:.3f}s")

        agent_duration = test_agents_login(context)

        print(f"Agents login navigation took {agent_duration:.3f}s")

        # Wait for 10 seconds to observe the logged-in state
        time.sleep(10)

        # Close the browser
        print("Closing browser...")
        browser.close()


if __name__ == "__main__":
    test_basic_functionality()