import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

BASE_API_URL: str = "https://api.kinopoisk.dev/v1.4"
BASE_UI_URL: str = "https://www.kinopoisk.ru/"

API_KEY: str = os.getenv("KINOPOISK_API_KEY", "").strip()


def get_auth_headers() -> dict:
    """
    Сформировать заголовки авторизации для запросов к API Кинопоиска.

    Returns:
        dict: Словарь HTTP-заголовков с токеном, если он задан.
    """
    headers: dict = {"Accept": "application/json"}
    if API_KEY:
        headers["x-api-key"] = API_KEY
    return headers
