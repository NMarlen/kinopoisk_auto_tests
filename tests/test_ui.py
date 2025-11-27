import allure
import pytest

from data.test_data import CYRILLIC_QUERY, DIGIT_QUERY
from pages.search_page import SearchPage


# Все тесты в этом файле относятся к UI
pytestmark = pytest.mark.ui


@allure.feature("UI: поиск фильмов")
@allure.title("Поиск фильма по названию на кириллице")
@allure.description(
    "Проверка, что поиск по запросу 'Нэчжа' возвращает хотя бы один результат."
)
def test_ui_search_by_cyrillic_query(driver) -> None:
    page = SearchPage(driver)
    page.open_main_page()
    page.search(CYRILLIC_QUERY)

    count = page.get_results_count()

    with allure.step("Проверить, что поисковая выдача не пустая"):
        assert count > 0


@allure.feature("UI: поиск фильмов")
@allure.title("Поиск фильма по цифровому запросу")
@allure.description(
    "Проверка, что поиск по запросу '11' возвращает хотя бы один фильм."
)
def test_ui_search_by_digits(driver) -> None:
    page = SearchPage(driver)
    page.open_main_page()
    page.search(DIGIT_QUERY)

    count = page.get_results_count()

    with allure.step("Проверить, что есть результаты поиска"):
        assert count > 0


@allure.feature("UI: поиск фильмов")
@allure.title("Открытие страницы первого фильма из выдачи")
@allure.description(
    "Проверка, что при клике по первому результату открывается карточка фильма."
)
def test_ui_open_first_result(driver) -> None:
    page = SearchPage(driver)
    page.open_main_page()
    page.search(CYRILLIC_QUERY)

    with allure.step("Клик по первому результату"):
        driver.find_element(*page.FIRST_RESULT_TITLE).click()

    with allure.step("Проверить, что открыта карточка фильма или сериала"):
        current_url = driver.current_url

        # Кинопоиск перекинул на showcaptcha
        # поэтому будем считать, что тест заблокирован защитой и скипаем его.
        if "showcaptcha" in current_url:
            pytest.skip("Кинопоиск вернул showcaptcha — тест заблокирован защитой сайта")

        assert "film" in current_url or "series" in current_url


@allure.feature("UI: поисковая строка")
@allure.title("Проверка наличия поля поиска на главной странице")
@allure.description(
    "Проверка, что поле поиска отображается при загрузке главной страницы."
)
def test_ui_search_input_visible(driver) -> None:
    page = SearchPage(driver)
    page.open_main_page()

    with allure.step("Проверить, что поле поиска отображается"):
        assert page.is_search_input_visible(), (
            "Поле поиска не найдено на главной странице"
        )


@allure.feature("UI: поиск фильмов")
@allure.title("Повторный поиск без перезагрузки страницы")
@allure.description(
    "Проверка, что можно выполнить два поиска подряд на одной странице."
)
def test_ui_two_searches_in_row(driver) -> None:
    page = SearchPage(driver)
    page.open_main_page()

    page.search(CYRILLIC_QUERY)
    first_count = page.get_results_count()

    page.search(DIGIT_QUERY)
    second_count = page.get_results_count()

    with allure.step("Проверить, что оба запроса возвращают результаты"):
        assert first_count > 0
        assert second_count > 0
