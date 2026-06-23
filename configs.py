# Browser
BROWSER_CHANNEL = "chrome"
HEADLESS = False
OBSERVATION_DELAY_SECONDS = 10

# Navigation
MAXIMUM_DURATION = 20  # seconds
NAVIGATION_TIMEOUT_MS = 21000 # milliseconds

# Thresholds
DEFAULT_DURATION_THRESHOLD = 20

# Savers Portal
SAVERS_SMS_BUTTON_TEXT = "סמס "
SAVERS_CONTINUE_BUTTON_TEXT = " המשך "

SAVERS_ID_FIELD = "idNumber"
SAVERS_PHONE_FIELD = "phone"

SAVERS_2FA_INPUT_IDS = [
    "ontimeInput1",
    "ontimeInput2",
    "ontimeInput3",
    "ontimeInput4",
    "ontimeInput5",
    "ontimeInput6",
]

# Agents Portal
AGENTS_USERNAME_FIELD = "UserName"
AGENTS_PASSWORD_FIELD = "Password"
AGENTS_TOKEN_FIELD = "CodeToken"
AGENTS_LOGIN_BUTTON_ID = "btnLoginSubmit"

# EMP Portal
EMP_USERNAME_FIELD = "txtUsername"
EMP_TOKEN_FIELD = "txtToken"
EMP_LOGIN_BUTTON_NAME = "btnNext"

# User Prompts
PROMPT_PHONE_READY = (
    "Get your phone ready to receive 2FA code, then press Enter to continue..."
)
PROMPT_2FA_RECEIVED = "Press Enter when you receive the 2FA code..."
PROMPT_2FA_CODE = "Enter the 2FA code: "
PROMPT_INVALID_2FA = "Invalid 2FA code, please try again."
PROMPT_COMSIGN_TOKEN = "Enter the ComSign token: "

# Messages
MSG_BROWSER_LAUNCH = "Launching browser..."
MSG_BROWSER_CLOSE = "Closing browser..."
MSG_DURATION_EXCEEDED = "Duration exceeded threshold, re-running the test..."