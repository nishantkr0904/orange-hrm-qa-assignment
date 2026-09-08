"""Reusable Selenium primitives used by every page object."""

from __future__ import annotations

import platform

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Base class that centralises explicit waits and browser interactions."""

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str]) -> None:
        element = self.find_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()

    def hover_and_click(self, locator: tuple[str, str]) -> None:
        """Match menu navigation that first requires pointer hover."""
        element = self.find_clickable(locator)
        ActionChains(self.driver).move_to_element(element).click().perform()

    def type_text(self, locator: tuple[str, str], value: str) -> None:
        element = self.find_visible(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        element.click()
        select_all_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        element.send_keys(select_all_key, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(value)

    def is_visible(self, locator: tuple[str, str]) -> bool:
        try:
            self.find_visible(locator)
            return True
        except Exception:
            return False
