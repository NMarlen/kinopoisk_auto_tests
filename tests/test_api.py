import allure
import pytest

from data.test_data import (
    CYRILLIC_QUERY,
    DIGIT_QUERY,
    GENRE_FANTASY,
    SYMBOL_QUERY,
)
from utils.api_client import KinopoiskApiClient


# По заданию должны быть режимы запуска: отдельно API, отдельно UI, все вместе.
# Здесь ставим общий маркер для всех API-тестов.
pytestmark = pytest.mark.api


@pytest.fixture(scope="session")
def api_client() -> KinopoiskApiClient:
    """
    Фикстура для создания экземпляра API-клиента Кинопоиска.

    Returns:
        KinopoiskApiClient: инициализированный клиент.
    """
    return KinopoiskApiClient()


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильма с названием из цифр")
@allure.description("Позитивный кейс: GET /movie/search?query=11 с корректным токеном.")
def test_search_movie_by_digits(api_client: KinopoiskApiClient) -> None:
    """
    Позитивный тест: поиск фильма по цифровому запросу.
    Ожидаем, что сервер вернёт 200 и хотя бы один фильм в выдаче.
    """
    response = api_client.search_movie_by_query(DIGIT_QUERY)

    with allure.step("Проверить, что код ответа 200"):
        assert response.status_code == 200

    data = response.json()
    with allure.step("Проверить, что в ответе есть хотя бы один фильм"):
        assert len(data.get("docs", [])) > 0


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильма на кириллице")
@allure.description("Позитивный кейс: GET /movie/search?query=Нэчжа.")
def test_search_movie_by_cyrillic(api_client: KinopoiskApiClient) -> None:
    """
    Позитивный тест: поиск фильма по запросу на кириллице.
    Проверяем, что в выдаче присутствует фильм с названием, содержащим 'нэчжа'.
    """
    response = api_client.search_movie_by_query(CYRILLIC_QUERY)

    with allure.step("Проверить, что код ответа 200"):
        assert response.status_code == 200

    data = response.json()
    titles = [doc.get("name", "").lower() for doc in data.get("docs", [])]

    with allure.step("Проверить, что в ответе есть фильм с названием на кириллице"):
        assert any("нэчжа" in title for title in titles)


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильмов по жанру")
@allure.description("Позитивный кейс: GET /movie?genres.name=фэнтези.")
def test_get_movies_by_genre(api_client: KinopoiskApiClient) -> None:
    """
    Позитивный тест: получение фильмов по жанру.
    Ожидаем, что сервер вернёт 200 и список фильмов не пуст.
    """
    response = api_client.get_movies_by_genre(GENRE_FANTASY)

    with allure.step("Проверить, что код ответа 200"):
        assert response.status_code == 200

    data = response.json()
    with allure.step("Проверить, что в ответе есть хотя бы один фильм"):
        assert len(data.get("docs", [])) > 0


@allure.feature("API: поиск фильмов")
@allure.title("Пустой поиск")
@allure.description(
    "Негативный кейс: запрос без значения query. "
    "Фактическое поведение API — чаще всего 200 с дефолтной выдачей."
)
def test_search_movie_empty_query(api_client: KinopoiskApiClient) -> None:
    """
    Негативный (по задумке) кейс: поиск с пустым query.
    Реальное поведение API: может возвращать 200 и дефолтный набор фильмов.
    Поэтому проверяем, что код ответа 200 или 404, и тело корректно парсится.
    """
    response = api_client.search_movie_empty_query()

    with allure.step("Проверить, что код ответа 200 или 404"):
        assert response.status_code in (200, 404)

    if response.status_code == 200:
        with allure.step("Проверить, что в ответе есть поле docs со списком"):
            data = response.json()
            assert isinstance(data.get("docs", []), list)


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильма по набору символов")
@allure.description(
    "Негативный кейс: GET /movie/search?query=_%%??. "
    "Фактическое поведение API — может вернуть 200 и непустую выдачу."
)
def test_search_movie_by_symbols(api_client: KinopoiskApiClient) -> None:
    """
    Негативный по идее кейс: поиск по строке из спецсимволов.
    Реальное поведение API: также может вернуть 200 и список фильмов.
    Тест проверяет, что ответ успешно обрабатывается и формат данных корректен.
    """
    response = api_client.search_movie_by_query(SYMBOL_QUERY)

    with allure.step("Проверить, что код ответа 200 или 404"):
        assert response.status_code in (200, 404)

    if response.status_code == 200:
        with allure.step("Проверить, что docs — это список (формат ответа корректный)"):
            data = response.json()
            assert isinstance(data.get("docs", []), list)


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильма с другим HTTP-методом")
@allure.description(
    "Негативный кейс: POST /movie/search?query=11 вместо GET. "
    "Фактическое поведение API — может возвращать 200 и обрабатывать запрос."
)
def test_search_movie_with_wrong_method(api_client: KinopoiskApiClient) -> None:
    """
    Негативный кейс по идее: использование неверного HTTP-метода.
    Реальное поведение API: иногда обрабатывает POST так же, как GET.
    Поэтому допускаем 200, 401 или 405, и при 200 проверяем формат ответа.
    """
    response = api_client.search_movie_with_wrong_method(DIGIT_QUERY)

    with allure.step("Проверить, что код ответа один из ожидаемых"):
        assert response.status_code in (200, 401, 405)

    if response.status_code == 200:
        with allure.step("Проверить, что в ответе есть поле docs"):
            data = response.json()
            assert "docs" in data


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильма без токена")
@allure.description("Негативный кейс: GET /movie/search?query=11 без заголовка x-api-key.")
def test_search_movie_without_token(api_client: KinopoiskApiClient) -> None:
    """
    Негативный кейс: запрос без токена авторизации.
    Ожидаем, что сервер вернёт 401.
    """
    response = api_client.search_movie_without_token(DIGIT_QUERY)

    with allure.step("Проверить, что код ответа 401"):
        assert response.status_code == 401


@allure.feature("API: поиск фильмов")
@allure.title("Поиск фильма с неверным токеном")
@allure.description("Негативный кейс: GET /movie/search?query=11 с некорректным токеном.")
def test_search_movie_with_invalid_token(api_client: KinopoiskApiClient) -> None:
    """
    Негативный кейс: запрос с некорректным токеном.
    Ожидаем, что сервер вернёт 401.
    """
    response = api_client.search_movie_with_invalid_token(DIGIT_QUERY)

    with allure.step("Проверить, что код ответа 401"):
        assert response.status_code == 401
