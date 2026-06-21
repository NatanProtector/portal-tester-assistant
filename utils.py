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

def get_button_by_text(page, text, exact=True):
    """
    Find a button by its visible text.

    Args:
        page: Playwright page object
        text: Text to search for
        exact: Whether to require an exact text match

    Returns:
        Playwright locator or None
    """
    if exact:
        button = page.get_by_role("button", name=text, exact=True)
    else:
        button = page.get_by_role("button", name=text)

    if button.count() > 0:
        return button

    # Search inside iframes
    for frame in page.frames:
        if exact:
            button = frame.get_by_role("button", name=text, exact=True)
        else:
            button = frame.get_by_role("button", name=text)

        if button.count() > 0:
            return button

    return None