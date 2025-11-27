# kinopoisk_auto_tests
# Автоматизация тестирования Кинопоиска

Проект содержит UI- и API-автотесты для сервиса Кинопоиск, выполненные в рамках финальной работы по автоматизации.
Используемый стек: pytest, selenium, requests, allure-pytest.

## Структура

- `data/` — конфигурация и тестовые данные:
  - `config.py` — базовые URL, чтение API-токена из `.env`.
  - `test_data.py` — значения запросов и тестовых параметров.
- `utils/`:
  - `api_client.py` — клиент для работы с API Кинопоиска.
- `pages/` — PageObject-страницы для UI:
  - `base_page.py` — базовый класс.
  - `search_page.py` — страница поиска.
- `tests/`:
  - `test_api.py` — API-тесты (по тест-кейсам из Qase).
  - `test_ui.py` — UI-тесты (по чек-листу финального проекта).
- `conftest.py` — фикстура `driver` для Selenium.
- `pytest.ini` — описание маркеров.
- `requirements.txt` — зависимости проекта.

## Установка

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Ссылка на фильнальный проект по ручному тестированию: 
https://portfolio-v.yonote.ru/share/39a1f025-5ac4-451c-ad91-06170d9efa78
