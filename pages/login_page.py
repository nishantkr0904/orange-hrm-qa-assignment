"""Page object for OrangeHRM's login and logout controls."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h6.oxd-text--h6")
    PROFILE_MENU = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[normalize-space()='Logout']")

    def load(self) -> None:
        self.open(self.URL)
        self.find_visible(self.USERNAME)

    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        self.wait.until(EC.url_contains("/dashboard"))
        self.find_visible(self.DASHBOARD_HEADER)

    def logout(self) -> None:
        self.click(self.PROFILE_MENU)
        self.click(self.LOGOUT_LINK)
        self.wait.until(EC.url_contains("/auth/login"))
        self.find_visible(self.USERNAME)
