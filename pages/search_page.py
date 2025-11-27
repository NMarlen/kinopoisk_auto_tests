from typing import Tuple

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC  # type: ignore[import]

from pages.base_page import BasePage


class SearchPage(BasePage):
    """
    PageObject для главной страницы и страницы поиска Кинопоиска.
    """

    # Главная страница
    URL = "https://www.kinopoisk.ru/"

    # Очень общий локатор для любого input на странице
    SEARCH_INPUT: Tuple[str, str] = (By.XPATH, "//input")

    # Ссылки на карточки фильмов/сериалов в выдаче
    FIRST_RESULT_TITLE: Tuple[str, str] = (
        By.CSS_SELECTOR,
        'a[href*="/film/"], a[href*="/series/"]',
    )

    RESULTS_TITLES: Tuple[str, str] = (
        By.CSS_SELECTOR,
        'a[href*="/film/"], a[href*="/series/"]',
    )

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    @allure.step("Открыть главную страницу Кинопоиска")
    def open_main_page(self) -> None:
        """
        Открывает главную страницу Кинопоиска.
        """
        self.open(self.URL)

    @allure.step('Открыть страницу поиска по запросу: "{query}"')
    def search(self, query: str) -> None:
        """
        Выполнить поиск фильма, переходя сразу на страницу результатов
        через URL с параметром kp_query.

        Args:
            query (str): поисковый запрос.
        """
        search_url = f"https://www.kinopoisk.ru/index.php?kp_query={query}"
        self.open(search_url)

    @allure.step("Получить количество результатов в выдаче")
    def get_results_count(self) -> int:
        """
        Возвращает количество видимых карточек фильмов/сериалов в выдаче.

        Returns:
            int: число найденных элементов.
        """
        elements = self.driver.find_elements(*self.RESULTS_TITLES)
        return len(elements)

    @allure.step("Проверить, что поле поиска отображается")
    def is_search_input_visible(self) -> bool:
        """
        Проверяет, что на странице есть хотя бы одно видимое поле ввода.

        Returns:
            bool: True, если найден и виден хотя бы один input.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
            return True
        except Exception:
            return False
