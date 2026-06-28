# Script for testing the basic functionality needed for the project
import os
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from utils import (
    apply_input,
    get_element_by_id,
    get_element_by_name,
    get_element_by_text,
    get_input_by_id,
    parse_args,
    code_is_valid,
)

# ============================================================================
# Constants
# ============================================================================
from configs import (
    MAXIMUM_DURATION,
    BROWSER_CHANNEL,
    HEADLESS,
    OBSERVATION_DELAY_SECONDS,
    DEFAULT_DURATION_THRESHOLD,
    SAVERS_SMS_BUTTON_TEXT,
    SAVERS_CONTINUE_BUTTON_TEXT,
    SAVERS_ID_FIELD,
    SAVERS_PHONE_FIELD,
    SAVERS_2FA_INPUT_IDS,
    AGENTS_USERNAME_FIELD,
    AGENTS_PASSWORD_FIELD,
    AGENTS_TOKEN_FIELD,
    AGENTS_LOGIN_BUTTON_ID,
    EMP_USERNAME_FIELD,
    EMP_TOKEN_FIELD,
    EMP_LOGIN_BUTTON_NAME,
    PROMPT_PHONE_READY,
    PROMPT_2FA_RECEIVED,
    PROMPT_2FA_CODE,
    PROMPT_INVALID_2FA,
    PROMPT_INVALID_TOKEN,
    PROMPT_COMSIGN_TOKEN,
    MSG_BROWSER_LAUNCH,
    MSG_BROWSER_CLOSE,
    MSG_DURATION_EXCEEDED,
)
# ============================================================================

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
    print("Testing Savers Page")
    savers_page = context.new_page()
    savers_page.goto(company_portal_savers_login)

    get_element_by_text(savers_page, SAVERS_SMS_BUTTON_TEXT).click()

    apply_input(savers_page, SAVERS_ID_FIELD, savers_id)
    apply_input(savers_page, SAVERS_PHONE_FIELD, savers_telephone)

    login_button = get_element_by_text(
        savers_page,
        SAVERS_CONTINUE_BUTTON_TEXT,
    )

    input(PROMPT_PHONE_READY)

    start = time.perf_counter()
    login_button.click()

    input(PROMPT_2FA_RECEIVED)

    two_fa_duration = time.perf_counter() - start

    two_fa_code = input(PROMPT_2FA_CODE)

    while not code_is_valid(two_fa_code):
        print(PROMPT_INVALID_2FA)
        two_fa_code = input(PROMPT_2FA_CODE)

    otp_inputs = [
        get_input_by_id(savers_page, input_id)
        for input_id in SAVERS_2FA_INPUT_IDS
    ]

    for index, otp_input in enumerate(otp_inputs[:-1]):
        otp_input.fill(two_fa_code[index])

    start = time.perf_counter()

    with savers_page.expect_navigation():
        otp_inputs[-1].fill(two_fa_code[-1])
        
    duration = time.perf_counter() - start

    savers_page.close()

    return two_fa_duration, duration


def test_agents_login(context):
    print("Testing Agents Page")

    agents_page = context.new_page()
    agents_page.goto(company_portal_agents_login)

    apply_input(
        agents_page,
        AGENTS_USERNAME_FIELD,
        agents_username,
    )
    apply_input(
        agents_page,
        AGENTS_PASSWORD_FIELD,
        agents_password,
    )

    token_input = get_element_by_id(
        agents_page,
        AGENTS_TOKEN_FIELD,
    )

    login_button = get_element_by_id(
        agents_page,
        AGENTS_LOGIN_BUTTON_ID,
    )

    token = input(PROMPT_COMSIGN_TOKEN)

    while not code_is_valid(token):
        print(PROMPT_INVALID_TOKEN)
        token = input(PROMPT_COMSIGN_TOKEN)

    token_input.fill(token)

    start = time.perf_counter()

    with agents_page.expect_navigation():
        login_button.click()

    duration = time.perf_counter() - start

    agents_page.close()

    return duration


def test_emp_login(context):
    print("Testing Employers Page")
    emp_page = context.new_page()
    emp_page.goto(company_portal_emp_login)

    apply_input(
        emp_page,
        EMP_USERNAME_FIELD,
        emp_username,
    )

    token_input = get_element_by_id(
        emp_page,
        EMP_TOKEN_FIELD,
    )

    login_button = get_element_by_name(
        emp_page,
        EMP_LOGIN_BUTTON_NAME,
    )

    token = input(PROMPT_COMSIGN_TOKEN)

    while not code_is_valid(token):
        print(PROMPT_INVALID_TOKEN)
        token = input(PROMPT_COMSIGN_TOKEN)

    token_input.fill(token)

    start = time.perf_counter()

    with emp_page.expect_navigation():
        login_button.click()

    duration = time.perf_counter() - start

    emp_page.close()

    return duration


def check_valid_duration(
    duration,
    test_func,
    context,
    threshold=DEFAULT_DURATION_THRESHOLD,
):
    if duration > threshold:
        print(MSG_DURATION_EXCEEDED)
        return test_func(context)

    return duration

def display_results(savers_duration_2FA, savers_duration_final, emp_duration, agent_duration):
    print(
            f"Agents login navigation took "
            f"{agent_duration:.3f}s"
        )

    print(
        f"\nSavers login: "
        f"2FA duration = {savers_duration_2FA:.3f}s, "
        f"final navigation duration = {savers_duration_final:.3f}s"
    )

    print(
        f"EMP login: navigation duration = "
        f"{emp_duration:.3f}s"
    )

    print(
        f"Agents login: navigation duration = "
        f"{agent_duration:.3f}s"
    )

def test_basic_functionality():
    args = parse_args()

    # If no flags were provided, run everything
    run_all = not any([
        args.emp,
        args.save,
        args.agents,
    ])

    with sync_playwright() as p:

        print(MSG_BROWSER_LAUNCH)

        browser = p.chromium.launch(
            channel=BROWSER_CHANNEL,
            headless=HEADLESS,
        )

        context = browser.new_context()

        savers_duration_2FA = None
        savers_duration_final = None
        emp_duration = None
        agent_duration = None

        # =========================
        # Savers
        # =========================
        if run_all or args.save:
            savers_duration_2FA, savers_duration_final = (
                test_savers_login(context)
            )

            if (
                savers_duration_2FA > MAXIMUM_DURATION
                or savers_duration_final > MAXIMUM_DURATION
            ):
                print(
                    f"Savers 2FA duration exceeded "
                    f"{MAXIMUM_DURATION}s, re-running the test..."
                )

                savers_duration_2FA, savers_duration_final = (
                    test_savers_login(context)
                )

            print(
                f"Savers login navigation took "
                f"{savers_duration_2FA:.3f}s for 2FA and "
                f"{savers_duration_final:.3f}s for final navigation"
            )

        # =========================
        # EMP
        # =========================
        if run_all or args.emp:
            emp_duration = test_emp_login(context)

            if emp_duration > MAXIMUM_DURATION:
                print(
                    f"EMP login navigation exceeded "
                    f"{MAXIMUM_DURATION}s, re-running the test..."
                )
                emp_duration = test_emp_login(context)

            print(
                f"EMP login navigation took "
                f"{emp_duration:.3f}s"
            )

        # =========================
        # Agents
        # =========================
        if run_all or args.agents:
            agent_duration = test_agents_login(context)

            if agent_duration > MAXIMUM_DURATION:
                print(
                    f"Agents login navigation exceeded "
                    f"{MAXIMUM_DURATION}s, re-running the test..."
                )
                agent_duration = test_agents_login(context)

            print(
                f"Agents login navigation took "
                f"{agent_duration:.3f}s"
            )

        # Display only executed tests
        print("\n=== Results ===")

        if (
            savers_duration_2FA is not None
            and savers_duration_final is not None
        ):
            print(
                f"Savers login: "
                f"2FA duration = {savers_duration_2FA:.3f}s, "
                f"final navigation duration = "
                f"{savers_duration_final:.3f}s"
            )

        if agent_duration is not None:
            print(
                f"Agents login navigation took "
                f"{agent_duration:.3f}s"
            )

        if emp_duration is not None:
            print(
                f"EMP login: navigation duration = "
                f"{emp_duration:.3f}s"
            )

        time.sleep(OBSERVATION_DELAY_SECONDS)

        print(MSG_BROWSER_CLOSE)
        browser.close()

if __name__ == "__main__":
    test_basic_functionality()