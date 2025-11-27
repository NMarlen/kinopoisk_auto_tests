from typing import Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    Базовый класс для всех PageObject-страниц.

    Содержит общие методы работы с WebDriver.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        """
        Открыть указанный URL в браузере.

        Args:
            url: Полный адрес страницы.
        """
        self.driver.get(url)

    def click(self, locator: tuple[By, str]) -> None:
        """
        Клик по элементу.

        Args:
            locator: Кортеж (By, locator_string).
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator: tuple[By, str], value: str, clear: bool = True) -> None:
        """
        Ввести текст в поле ввода.

        Args:
            locator: Кортеж (By, locator_string).
            value: Текст, который нужно ввести.
            clear: Нужно ли предварительно очищать поле.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(value)

    def get_text(
        self,
        locator: tuple[By, str],
        timeout: Optional[int] = None,
    ) -> str:
        """
        Получить текст элемента.

        Args:
            locator: Кортеж (By, locator_string).
            timeout: Переопределить таймаут ожидания.

        Returns:
            str: Текст элемента.
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def elements_count(self, locator: tuple[By, str]) -> int:
        """
        Подсчитать количество элементов по локатору.

        Args:
            locator: Кортеж (By, locator_string).

        Returns:
            int: Количество элементов.
        """
        elements = self.driver.find_elements(*locator)
        return len(elements)
