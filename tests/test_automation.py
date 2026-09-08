"""OrangeHRM end-to-end workflow implemented with Page Object Model."""

from __future__ import annotations

import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.pim_page import PimPage


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


def test_add_and_verify_employees(driver):
    username = os.getenv("ORANGEHRM_USERNAME", "Admin")
    password = os.getenv("ORANGEHRM_PASSWORD", "admin123")
    # Eight digits leave room below OrangeHRM's 10-character Employee ID limit.
    run_id = datetime.now().strftime("%H%M%S%f")[-7:]
    employees = [
        ("ABD", f"QA{run_id}A", f"{run_id}1"),
        ("MSD", f"QA{run_id}B", f"{run_id}2"),
        ("KING", f"QA{run_id}C", f"{run_id}3"),
        ("HITMAN", f"QA{run_id}D", f"{run_id}4"),
    ]

    login_page = LoginPage(driver)
    pim_page = PimPage(driver)
    login_page.load()
    login_page.login(username, password)

    try:
        pim_page.open_pim()
        created_employees = [
            pim_page.add_employee(first_name, last_name, employee_id)
            for first_name, last_name, employee_id in employees
        ]
        pim_page.open_employee_list()

        for employee in created_employees:
            assert pim_page.verify_employee(employee), (
                f"Employee was not found: {employee.full_name} "
                f"(ID: {employee.employee_id})"
            )
            print("Name Verified")
    finally:
        if "/dashboard" in driver.current_url or "/pim/" in driver.current_url:
            login_page.logout()
