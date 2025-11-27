from collections.abc import Generator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture(scope="session")
def driver() -> Generator[WebDriver, None, None]:
    """
    Сессионная фикстура WebDriver для UI-тестов.

    Создаёт экземпляр Chrome в headless-режиме и закрывает его по завершении
    всех тестов.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service()  # chromedriver берётся из PATH
    driver_instance: WebDriver = webdriver.Chrome(service=service, options=options)
    driver_instance.implicitly_wait(10)

    with allure.step("Инициализация WebDriver"):
        yield driver_instance

    with allure.step("Закрытие WebDriver"):
        driver_instance.quit()
