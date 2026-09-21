import json
import os
import random
from pathlib import Path
from time import sleep

from Browser.utils.data_types import DialogAction, SelectAttribute
from robocorp.tasks import task
from RPA.Browser.Playwright import Playwright
from RPA.Tables import Tables

browser_lib = Playwright()
BASE_URL = "https://qa-practice.razvanvancea.ro"
CSV_BASE_PATH = "output/csv"
STATE_FILE = Path("output/state.json")
table_lib = Tables()


#CHECKPOINTING 

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"completed_steps": []}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def mark_done(state, step_name):
    if step_name not in state["completed_steps"]:
        state["completed_steps"].append(step_name)
        save_state(state)


def is_done(state, step_name):
    return step_name in state["completed_steps"]


# MAIN WORKFLOW 

@task
def register_on_qa_practice():
    """Executes QA practice tasks with checkpointing support."""
    browser_lib.new_browser(
        headless=False,
        slowMo=0.4
    )
    browser_lib.new_page(BASE_URL)

    # Sequential workflow list 
    steps = [
        ("register_form", fill_and_submit_register_form),
        ("login", login),
        ("recover_password", recoverpassword),
        ("checkboxes_radiobuttons", checkbox_radiobox),
        ("content_window", contentwindow),
        ("double_click", doubleclick),
        ("scrolling", scrolling),
        ("mouse_hover", hoverwala),
        ("show_hide_element", show_hid),
        ("static_table_extract", extract_date_from_static),
        ("dynamic_table_extract", extract_dynamic_html_table_to_csv),
        ("dropdowns", drop_multi),
        ("iframe", iframe),
        ("alerts", alerat),
        ("file_upload", fileUP),
        ("calendar_picker", calendar_picker),
        ("loader", loader),
        ("pagination", pagnation),
        ("ecommerce", ecommerce),
    ]

    state = load_state()

    # Reset state if all steps finished in a previous run
    if len(state["completed_steps"]) >= len(steps):
        print("All steps were previously completed. Resetting state to start from Step 1...")
        state = {"completed_steps": []}
        save_state(state)

    for step_name, step_fn in steps:
        if is_done(state, step_name):
            print(f"Skipping {step_name} already completed.")
            continue

        print(f"Executing step: {step_name}")
        step_fn()
        mark_done(state, step_name)


#TASK STEP DEFINITIONS

def fill_and_submit_register_form():
    """Navigates to register page, fills in the form fields, and submits."""
    browser_lib.go_to(f"{BASE_URL}/register.html")
    
    browser_lib.type_text("#firstName", "Yogesh")
    browser_lib.type_text("#lastName", "Baral")
    browser_lib.type_text("#phone", "9800000000")
    browser_lib.select_options_by("#countries_dropdown_menu", SelectAttribute.value, "Nepal")
    browser_lib.type_text("#emailAddress", "yogesh.test@example.com")
    browser_lib.type_text("#password", "SuperSecret123!")

    browser_lib.check_checkbox("input[type='checkbox']")
    browser_lib.click("#registerBtn")


def login():
    """Navigates to login page and submits credentials."""
    browser_lib.go_to(f"{BASE_URL}/login.html")
    browser_lib.type_text("#email", "yogesh.test@example.com")
    browser_lib.type_text("#password", "SuperSecret123!")
    browser_lib.click("#submitLoginBtn")


def recoverpassword():
    """Navigates to password recovery and submits email."""
    browser_lib.go_to(f"{BASE_URL}/recover-password.html")
    browser_lib.type_text("#email", "yogesh.test@example.com")
    browser_lib.click("button#recover-password")


def checkbox_radiobox():
    """Demonstrates how to select checkboxes and radio buttons."""
    browser_lib.go_to(f"{BASE_URL}/checkboxes.html")
    for i in range(1, 4):
        browser_lib.check_checkbox(f"#checkbox{i}")
    browser_lib.click("button[type='reset']")
    
    browser_lib.go_to(f"{BASE_URL}/radiobuttons.html")
    browser_lib.check_checkbox("#radio-button2")
    browser_lib.check_checkbox("#radio-button3")
    browser_lib.evaluate_javascript("#radio-button4", "(elem) => elem.disabled = false")
    browser_lib.check_checkbox("#radio-button4")


def contentwindow():
    """Tests new tab and window creation."""
    browser_lib.go_to(f"{BASE_URL}/tab.html")
    browser_lib.click("#newTabBtn")
    browser_lib.switch_page("NEW")
    browser_lib.close_page()
    sleep(1)
    
    browser_lib.go_to(f"{BASE_URL}/window.html")
    browser_lib.click("#newWindowBtn")
    prev_page_id = browser_lib.switch_page("NEW")
    browser_lib.close_page()
    browser_lib.switch_page(prev_page_id)
    sleep(1)


def doubleclick():
    """Tests double clicking actions."""
    browser_lib.go_to(f"{BASE_URL}/double-click.html")
    browser_lib.click_with_options("#double-click-btn", clickCount=2)
    sleep(1)


def scrolling():
    """Tests element scrolling capabilities."""
    browser_lib.go_to(f"{BASE_URL}/scroll.html")
    browser_lib.scroll_to_element("#main")
    browser_lib.scroll_to_element("#the-end")
    sleep(1)


def hoverwala():
    """Tests hover interactions."""
    browser_lib.go_to(f"{BASE_URL}/mouse-hover.html")
    browser_lib.hover("#button-hover-over")
    sleep(1)


def show_hid():
    """Tests DOM property modification for showing/hiding elements."""
    browser_lib.go_to(f"{BASE_URL}/show-hide-element.html")
    browser_lib.evaluate_javascript("#hiddenText", "(elem) => elem.style.display = 'none'")
    sleep(1)
    browser_lib.evaluate_javascript("#hiddenText", "el=>el.style.setProperty('display', 'block')")
    sleep(1)


def extract_date_from_static():
    """Extracts a static HTML table and saves it as CSV."""
    browser_lib.go_to(f"{BASE_URL}/web-table.html")

    column = []
    for i in range(1, 5):
        data = browser_lib.get_text(f"#peopleTable > thead > tr > th:nth-child({i})")
        column.append(data)
    table_data = [column]

    for j in range(1, 6):
        new_row = []
        first_col_data = browser_lib.get_text(f"#peopleTable tbody tr:nth-child({j}) th")
        new_row.append(first_col_data)
        for k in range(2, 5):
            data = browser_lib.get_text(f"#peopleTable tbody tr:nth-child({j}) td:nth-child({k})")
            new_row.append(data)
        table_data.append(new_row)

    Path(CSV_BASE_PATH).mkdir(parents=True, exist_ok=True)
    table_lib.write_table_to_csv(
        table=table_lib.create_table(table_data),
        header=False,
        path=f"{CSV_BASE_PATH}/static_table.csv",
    )


def extract_dynamic_html_table_to_csv():
    """Extracts dynamic table data into output/csv directory."""
    browser_lib.go_to(f"{BASE_URL}/dynamic-table.html")
    Path(CSV_BASE_PATH).mkdir(parents=True, exist_ok=True)

    column = []
    header_selectors = browser_lib.get_elements("#data-table thead tr th")
    for header in header_selectors:
        column.append(browser_lib.get_text(header))

    table_data = [column]

    data_row_selectors = browser_lib.get_elements("#data-table tbody tr")
    for row in data_row_selectors:
        new_row = []
        cell_elements = browser_lib.get_elements(f"{row} >> td")
        for cell in cell_elements:
            new_row.append(browser_lib.get_text(cell))
        table_data.append(new_row)

    table = table_lib.create_table(table_data)
    table_lib.write_table_to_csv(table=table, header=False, path=f"{CSV_BASE_PATH}/dynamic_table.csv")


def drop_multi():
    """Interacts with dropdowns and hover items."""
    browser_lib.go_to(f"{BASE_URL}/dropdowns.html")
    browser_lib.select_options_by("#dropdown-menu", SelectAttribute.value, "Algeria")
    browser_lib.click("#multi-level-dropdown-btn")
    browser_lib.hover("text=Hover me for more options")
    browser_lib.hover("text=Even More..")
    browser_lib.hover("text=another level")
    sleep(1)


def iframe():
    """Interacts with iframe embedded controls."""
    browser_lib.go_to(f"{BASE_URL}/iframe.html")
    browser_lib.click("iframe >>> #learn-more")


def alerat():
    """Handles browser dialog alerts and confirms."""
    browser_lib.go_to(f"{BASE_URL}/alerts.html")

    browser_lib.handle_future_dialogs(action=DialogAction.accept)
    browser_lib.click("#alert-btn")
    sleep(1)

    browser_lib.close_page()
    browser_lib.new_page(f"{BASE_URL}/alerts.html")

    browser_lib.handle_future_dialogs(action=DialogAction.accept)
    browser_lib.click("#confirm-btn")
    sleep(1)


def fileUP():
    """Handles file selection and submission."""
    browser_lib.go_to(f"{BASE_URL}/file-upload.html")

    file_path = os.path.expanduser("/Users/yogesh/Downloads/orders.csv")

    promise = browser_lib.promise_to_upload_file(file_path)
    browser_lib.click("#file_upload")
    browser_lib.wait_for(promise)

    sleep(1)
    browser_lib.click("button[type='submit']")


def calendar_picker():
    """Interacts with date range picker fields."""
    browser_lib.go_to(f"{BASE_URL}/calendar.html")
    browser_lib.fill_text("#range-date-calendar", "01/01/2026 - 01/15/2026")
    browser_lib.fill_text("#calendar", "09/15/2026")
    browser_lib.press_keys("#calendar", "Enter")
    sleep(1)


def loader():
    """Waits dynamically for dynamic loading elements."""
    browser_lib.go_to(f"{BASE_URL}/loader.html")
    browser_lib.wait_for_elements_state("text=Tada!", timeout="10s")
    sleep(1)


def pagnation():
    """Navigates pagination links safely."""
    browser_lib.go_to(f"{BASE_URL}/pagination.html")

    browser_lib.click('a[onclick="showPageNumber(1)"]')
    sleep(0.5)

    browser_lib.click('a[onclick="showPageNumber(2)"]')
    sleep(0.5)

    browser_lib.click("li.page-item:not(.disabled) >> text=Next")
    sleep(0.5)


def ecommerce():
    """Completes an e-commerce checkout flow."""
    browser_lib.go_to(f"{BASE_URL}/auth_ecommerce.html")
    browser_lib.type_text("#email", "admin@admin.com")
    browser_lib.type_text("#password", "admin123")
    browser_lib.click("#submitLoginBtn")
    sleep(1)

    add_to_cart_count = browser_lib.get_element_count(".shop-items button")
    random_index = random.randint(0, add_to_cart_count - 1)

    browser_lib.click(f".shop-items button >> nth={random_index}")
    sleep(0.5)

    browser_lib.click("text=PROCEED TO CHECKOUT")
    browser_lib.type_text("#phone", "980000")
    browser_lib.type_text("[name='street']", "Kathmandu Street 12")
    browser_lib.type_text("[name='city']", "Kathmandu")
    browser_lib.select_options_by("#countries_dropdown_menu", SelectAttribute.value, "Nepal")
    browser_lib.click("#submitOrderBtn")
    sleep(1)