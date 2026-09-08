"""Page object for adding and locating employees in the PIM module."""

from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


@dataclass(frozen=True)
class Employee:
    """The immutable record needed to find a newly created employee."""

    first_name: str
    last_name: str
    employee_id: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class PimPage(BasePage):
    PIM_MENU = (By.XPATH, "//span[normalize-space()='PIM']/ancestor::a")
    ADD_EMPLOYEE_LINK = (By.XPATH, "//a[normalize-space()='Add Employee']")
    EMPLOYEE_LIST_LINK = (By.XPATH, "//a[normalize-space()='Employee List']")
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    EMPLOYEE_ID = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']"
        "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), "
        "' oxd-input-group ')][1]//input",
    )
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    EMPLOYEE_ID_SEARCH = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']"
        "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), "
        "' oxd-input-group ')][1]//input",
    )
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    FIELD_VALIDATION_ERRORS = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

    def open_pim(self) -> None:
        self.hover_and_click(self.PIM_MENU)
        self.wait.until(EC.url_contains("/pim/"))

    def add_employee(
        self, first_name: str, last_name: str, employee_id: str
    ) -> Employee:
        """Create an employee with a test-controlled unique Employee ID."""
        if not employee_id.isdigit() or len(employee_id) > 10:
            raise ValueError("Employee ID must contain at most 10 numeric characters.")

        self.click(self.ADD_EMPLOYEE_LINK)
        self.find_visible(self.FIRST_NAME)
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.EMPLOYEE_ID, employee_id)
        entered_id = self.find_visible(self.EMPLOYEE_ID).get_attribute("value")
        if entered_id != employee_id:
            raise AssertionError(
                f"Employee ID entry failed: expected {employee_id}, got {entered_id!r}."
            )
        self.click(self.SAVE_BUTTON)

        def save_completed_or_failed(driver):
            if "/pim/viewPersonalDetails" in driver.current_url:
                return True

            errors = [
                error.text.strip()
                for error in driver.find_elements(*self.FIELD_VALIDATION_ERRORS)
                if error.is_displayed() and error.text.strip()
            ]
            return errors or False

        result = self.wait.until(save_completed_or_failed)
        if result is not True:
            raise AssertionError(
                f"OrangeHRM rejected employee {employee_id}: {', '.join(result)}"
            )
        return Employee(first_name, last_name, employee_id)

    def open_employee_list(self) -> None:
        self.click(self.EMPLOYEE_LIST_LINK)
        self.wait.until(EC.url_contains("/pim/viewEmployeeList"))
        self.find_visible(self.EMPLOYEE_ID_SEARCH)

    def verify_employee(self, employee: Employee) -> bool:
        """Locate a new employee by unique ID and verify the displayed name."""
        self.type_text(self.EMPLOYEE_ID_SEARCH, employee.employee_id)
        self.click(self.SEARCH_BUTTON)
        row = (
            By.XPATH,
            "//div[contains(@class, 'oxd-table-card')]"
            f"[contains(., '{employee.employee_id}')]",
        )
        element = self.find_visible(row)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        row_text = element.text
        return (
            employee.employee_id in row_text
            and employee.first_name in row_text
            and employee.last_name in row_text
        )
