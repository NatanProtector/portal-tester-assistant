import time

def get_element_by_id(page, element_id):
    """
    Locate an element by ID, searching through the main page and all iframes.
    
    Args:
        page: The Playwright page object
        element_id: The ID of the element to find (with or without '#')
    
    Returns:
        The located element, or None if not found
    """
    # Ensure ID has '#' prefix
    if not element_id.startswith('#'):
        element_id = f'#{element_id}'
    
    # Check main page first
    main_element = page.locator(element_id)
    if main_element.count() > 0:
        return main_element
    
def get_input_by_id(page, element_id):
    """
    Locate an input element by ID, searching through the main page and all iframes.
    
    Args:
        page: The Playwright page object
        element_id: The ID of the input element to find (with or without '#')
    
    Returns:
        The located input element, or None if not found
    """
        # Ensure ID has '#' prefix
    if not element_id.startswith('#'):
        element_id = f'input#{element_id}'
    
    # Check main page first
    main_element = page.locator(element_id)
    if main_element.count() > 0:
        return main_element

def get_element_by_name(page, element_name):
    """
    Locate an element by name, searching through the main page and all iframes.

    Args:
        page: The Playwright page object
        element_name: The name attribute of the element to find

    Returns:
        The located element, or None if not found
    """
    selector = f'[name="{element_name}"]'

    # Check main page first
    main_element = page.locator(selector)
    if main_element.count() > 0:
        return main_element

    # Check all iframes
    for frame in page.frames:
        try:
            frame_element = frame.locator(selector)
            if frame_element.count() > 0:
                return frame_element
        except Exception:
            pass

    return None

def get_element_by_text(page, text):
    """
    Locate an element by its text content, searching through the main page and all iframes.

    Args:
        page: The Playwright page object
        text: The text content to search for
    Returns:
        The located element, or None if not found
    """
    selector = f'text="{text}"'

    # Check main page first
    main_element = page.locator(selector)
    if main_element.count() > 0:
        return main_element

    # Check all iframes
    for frame in page.frames:
        try:
            frame_element = frame.locator(selector)
            if frame_element.count() > 0:
                return frame_element
        except Exception:
            pass

    return None

def apply_input(page, id, value, delay=0.5, component_timeout_ms=10000):
    element = get_element_by_id(page, f"#{id}")
    if element:
        element.wait_for(state="visible", timeout=component_timeout_ms)
        element.fill(value)
        element.press("Tab")  # Trigger blur/change event
    else:
        raise ValueError("Element not found")
    time.sleep(delay)  # Small delay after click
    return element

def click_element(page, id, delay=0.5, component_timeout_ms=10000):
    element = get_element_by_id(page, f"#{id}")
    if element:
        element.wait_for(state="visible", timeout=component_timeout_ms)
        element.click(timeout=component_timeout_ms)
    else:
        raise ValueError("Element not found")
    time.sleep(delay)  # Small delay after click
    return element

def two_fa_code_is_valid(code):
    return code.isdigit() and len(code) == 6