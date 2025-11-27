from typing import Any, Dict

import allure
import requests

from data.config import BASE_API_URL, get_auth_headers
from data.test_data import INVALID_TOKEN


class KinopoiskApiClient:
    """
    Клиент для работы с API Кинопоиска v1.4.

    Все методы возвращают объект requests.Response.
    """

    def __init__(self) -> None:
        self.base_url: str = BASE_API_URL

    @allure.step("GET /movie/search c query='{query}' и корректным токеном")
    def search_movie_by_query(self, query: str) -> requests.Response:
        """
        Поиск фильма по строке запроса.

        Args:
            query: Строка запроса для параметра `query`.

        Returns:
            requests.Response: HTTP-ответ API.
        """
        url: str = f"{self.base_url}/movie/search"
        headers: Dict[str, str] = get_auth_headers()
        params: Dict[str, Any] = {"query": query}
        response = requests.get(url, headers=headers, params=params, timeout=15)
        return response

    @allure.step("GET /movie по жанру '{genre_name}'")
    def get_movies_by_genre(self, genre_name: str) -> requests.Response:
        """
        Получить список фильмов по жанру.

        Args:
            genre_name: Название жанра на русском.

        Returns:
            requests.Response: HTTP-ответ API.
        """
        url: str = f"{self.base_url}/movie"
        headers: Dict[str, str] = get_auth_headers()
        params: Dict[str, Any] = {"genres.name": genre_name}
        response = requests.get(url, headers=headers, params=params, timeout=15)
        return response

    @allure.step("GET /movie/search c пустым query-параметром")
    def search_movie_empty_query(self) -> requests.Response:
        """
        Поиск фильма с пустым параметром query.

        Returns:
            requests.Response: HTTP-ответ API.
        """
        url: str = f"{self.base_url}/movie/search"
        headers: Dict[str, str] = get_auth_headers()
        # query без значения → ?query
        response = requests.get(f"{url}?query", headers=headers, timeout=15)
        return response

    @allure.step("POST /movie/search c query='{query}' вместо GET")
    def search_movie_with_wrong_method(self, query: str) -> requests.Response:
        """
        Отправка запроса с некорректным HTTP-методом.

        Args:
            query: Строка запроса.

        Returns:
            requests.Response: HTTP-ответ API.
        """
        url: str = f"{self.base_url}/movie/search"
        headers: Dict[str, str] = get_auth_headers()
        params: Dict[str, Any] = {"query": query}
        response = requests.post(url, headers=headers, params=params, timeout=15)
        return response

    @allure.step("GET /movie/search c query='{query}' и без токена авторизации")
    def search_movie_without_token(self, query: str) -> requests.Response:
        """
        Поиск фильма без передачи токена авторизации.

        Args:
            query: Строка запроса.

        Returns:
            requests.Response: HTTP-ответ API.
        """
        url: str = f"{self.base_url}/movie/search"
        params: Dict[str, Any] = {"query": query}
        response = requests.get(url, params=params, timeout=15)
        return response

    @allure.step("GET /movie/search c query='{query}' и неверным токеном")
    def search_movie_with_invalid_token(self, query: str) -> requests.Response:
        """
        Поиск фильма с некорректным токеном авторизации.

        Args:
            query: Строка запроса.

        Returns:
            requests.Response: HTTP-ответ API.
        """
        url: str = f"{self.base_url}/movie/search"
        headers: Dict[str, str] = get_auth_headers()
        headers["x-api-key"] = INVALID_TOKEN
        params: Dict[str, Any] = {"query": query}
        response = requests.get(url, headers=headers, params=params, timeout=15)
        return response
