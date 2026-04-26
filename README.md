# API автотесты для практикума SDET

Проект выполнен в рамках задания «Практикум SDET: задание API».

## Объект тестирования

Локально развёрнутое тестовое приложение:

```commandline
http://localhost:8080
```

Swagger

```commandline
http://localhost:8080/api/_/docs/swagger/index.html#/
```

## Описание проекта

В проекте реализованы API-автотесты для проверки всех основных точек доступа тестового приложения.

Автотесты покрывают положительные сценарии работы с сущностью:

- создание сущности
- получение сущности по id
- получение списка сущностей
- обновление сущности
- удаление сущности

### Технологии

- Python 3.10
- pytest
- requests
- pydantic
- Allure Report
- pytest-xdist

---

## Что реализовано

### API-клиент

Для работы с API создан отдельный класс `EntityApi`.

В API-клиенте реализованы методы:

- `create_entity` — отправляет POST-запрос на создание сущности
- `get_entity` — отправляет GET-запрос на получение сущности по id
- `get_all_entities` — отправляет GET-запрос на получение списка сущностей
- `patch_entity` — отправляет PATCH-запрос на обновление сущности
- `delete_entity` — отправляет DELETE-запрос на удаление сущности

Эндпоинты вынесены в отдельный файл `endpoints.py`, чтобы не хардкодить URL прямо внутри тестов и методов API-клиента.

### Модели данных

Для формирования тела запроса используются Pydantic-модели:

- `AdditionRequest`
- `EntityRequest`

Для десериализации ответов используются Pydantic-модели:

- `CreateEntityResponse`
- `AdditionResponse`
- `EntityResponse`
- `GetAllEntitiesResponse`

Все полученные от API данные десериализуются в объекты моделей через `pydantic`.

### Тестовые данные

Payload для создания сущности собирается через функцию `build_entity_payload`.
Это позволяет не собирать тело запроса вручную в каждом тесте и держать структуру тестовых данных отдельно от тестовой
логики.

### Assertions

Общие проверки вынесены в отдельный файл `tests/api/assertions.py`.
Например, проверка соответствия полученной сущности отправленному payload выполняется через
helper-функцию `assert_entity_matches_payload`.

---

## Автотесты

В проекте реализованы 5 положительных API-тестов:

### 1. Создание сущности

Файл:

`tests/api/test_create_entity.py`

Проверяется сценарий:

1. Сформировать тело запроса для создания сущности.
2. Отправить POST-запрос на `/api/create`.
3. Проверить, что сервер вернул статус-код 200.
4. Проверить, что в ответе вернулся id созданной сущности.
5. Проверить, что id является числом.

### 2. Получение сущности по id

Файл:

`tests/api/test_get_entity.py`

Проверяется сценарий:

1. Создать сущность через API.
2. Отправить GET-запрос на `/api/get/{entity_id}`.
3. Проверить, что сервер вернул статус-код `200`.
4. Десериализовать ответ в модель `EntityResponse`.
5. Проверить, что id полученной сущности совпадает с id созданной сущности.
6. Проверить, что поля сущности соответствуют отправленному payload.

### 3. Получение списка сущностей

Файл:

`tests/api/test_get_all_entities.py`

Проверяется сценарий:

1. Создать сущность через API.
2. Отправить GET-запрос на `/api/getAll`.
3. Проверить, что сервер вернул статус-код `200`.
4. Десериализовать ответ в модель `GetAllEntitiesResponse`.
5. Проверить, что список сущностей не пустой.
6. Проверить, что созданная сущность присутствует в общем списке.

### 4. Обновление сущности

Файл:

`tests/api/test_patch_entity.py`

Проверяется сценарий:

1. Создать сущность через API.
2. Сформировать payload с обновлёнными данными.
3. Отправить PATCH-запрос на `/api/patch/{entity_id}`.
4. Проверить, что сервер вернул статус-код `204`.
5. Проверить, что тело ответа пустое.
6. Получить обновлённую сущность через GET-запрос.
7. Десериализовать ответ в модель `EntityResponse`.
8. Проверить, что данные сущности обновились.

### 5. Удаление сущности

Файл:

`tests/api/test_delete_entity.py`

Проверяется сценарий:

1. Создать сущность через API.
2. Отправить DELETE-запрос на `/api/delete/{entity_id}`.
3. Проверить, что сервер вернул статус-код `204`.
4. Проверить, что тело ответа пустое.

## Allure Report

В проект добавлено формирование Allure-отчётов.

В тестах используются:

* `@allure.feature`
* `@allure.story`
* `@allure.title`
* `allure.step`

Запуск тестов с генерацией Allure-results:

`pytest --alluredir=allure-results`

Открытие Allure-отчёта:

`allure serve allure-results`

---

## Параллельный запуск

В проект добавлен параллельный запуск тестов через `pytest-xdist`.

Рекомендуемая команда запуска:

`pytest -n 2 --dist=loadgroup`

Для тестов `Entity API` используется маркер `xdist_group("entity_api")`.

Это сделано для того, чтобы тесты, работающие с одним тестовым сервисом и общей базой данных, выполнялись в рамках одной
группы. Такой подход предотвращает конкурентные операции записи в БД, из-за которых тестовое приложение может возвращать
ошибки соединения с Postgres.

Команда для параллельного запуска с Allure:

`pytest -n 2 --dist=loadgroup --alluredir=allure-results`

Открытие отчёта:

`allure serve allure-results`

---

## Установка и запуск

### 1. Клонировать репозиторий

```commandline
git clone https://github.com/AmirRoni/SimbirSoft-SDET-Week-2.git
cd SimbirSoft-SDET-Week-2
```

### 2. Создать и активировать виртуальное окружение

Windows:

```commandline
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```commandline
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```commandline
pip install -r requirements.txt
```

### 4. Запустить тестовое приложение

Перед запуском тестов приложение должно быть доступно по адресу:

```commandline
http://localhost:8080
```
Если тестовое приложение запускается через Docker Compose:

```commandline
docker compose up -d
```

5. Запустить все тесты

Обычный запуск:

```
pytest
```

Параллельный запуск:

```
pytest -n 2 --dist=loadgroup
```

Запуск с Allure:

```
pytest --alluredir=allure-results
```

Параллельный запуск с Allure:

```
pytest -n 2 --dist=loadgroup --alluredir=allure-results
```

Открыть Allure-отчёт:

```
allure serve allure-results
```

## Покрытие по заданию

По заданию требуется создать проект из пяти API-автотестов для всех точек доступа к приложению.

В проекте реализованы 5 положительных API-автотестов:

* `POST /api/create`
* `GET /api/get/{entity_id}`
* `GET /api/getAll`
* `PATCH /api/patch/{entity_id}`
* `DELETE /api/delete/{entity_id}`

Дополнительно реализовано:

* формирование Allure-отчётов
* параллельный запуск тестов через `pytest-xdist`

## Полезные команды

Запуск конкретного тестового файла:

`pytest tests/api/test_create_entity.py`

Параллельный запуск:

`pytest -n 2 --dist=loadgroup`

Запуск тестов с Allure:

`pytest --alluredir=allure-results`

Параллельный запуск с Allure:

`pytest -n 2 --dist=loadgroup --alluredir=allure-results`

Открытие Allure-отчёта:

`allure serve allure-results`

Остановка Docker-контейнеров:

`docker compose down`

Полный сброс контейнеров и volumes:

`docker compose down -v`

Запуск тестового приложения:

`docker compose up -d`