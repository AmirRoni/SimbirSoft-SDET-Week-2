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

Исходный репозиторий тестового сервиса:

```
https://github.com/sun6r0/test-service
```

Тестовый сервис запускается через Docker Compose и включает:

- Go API-сервис
- PostgreSQL
- миграции базы данных

---

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
- GitHub Actions
- Docker Compose

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
3. Проверить, что сервер вернул статус-код `200`.
4. Десериализовать ответ в модель `CreateEntityResponse`.
5. Проверить, что в ответе вернулся id созданной сущности.
6. Проверить, что id является числом.

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

---

## Allure Report

В проект добавлено формирование Allure-отчётов.

В тестах используются:

- `@allure.feature`
- `@allure.story`
- `@allure.title`
- `allure.step`

Запуск тестов с генерацией Allure-results:

```
pytest --alluredir=allure-results
```

Открытие Allure-отчёта:

```
allure serve allure-results
```

Параллельный запуск с Allure:

```
pytest -n 2 --dist=loadgroup --alluredir=allure-
```

---

## Параллельный запуск

В проект добавлен параллельный запуск тестов через `pytest-xdist`.

Рекомендуемая команда запуска:

```
pytest -n 2 --dist=loadgroup
```

Для тестов `Entity API` используется маркер:

```
@pytest.mark.xdist_group("entity_api")
```

Это сделано для того, чтобы тесты, работающие с одним тестовым сервисом и общей базой данных, выполнялись в рамках одной группы.

Такой подход снижает риск конкурентных операций записи в БД, из-за которых тестовое приложение может возвращать ошибки соединения с PostgreSQL.

Параллельный запуск с Allure:

```
pytest -n 2 --dist=loadgroup --alluredir=allure-results
```

---

## CI/CD

В проект добавлен запуск API-автотестов в GitHub Actions.

Workflow-файл находится по пути:

```
.github/workflows/api-tests.yml
```

CI запускается:

- автоматически при создании Pull Request в ветку `main`
- вручную через вкладку **Actions** в GitHub

В CI выполняются шаги:

1. Клонируется репозиторий с автотестами.
2. Клонируется репозиторий тестового сервиса `sun6r0/test-service`.
3. Устанавливается Python 3.10.
4. Устанавливаются зависимости из `requirements.txt`.
5. Тестовый сервис запускается через Docker Compose.
6. Выполняются API-автотесты через `pytest`.
7. Allure-results сохраняются как artifact.
8. Docker-контейнеры останавливаются после завершения job.

Команда запуска тестов в CI:

```
pytest -n 2 --dist=loadgroup --alluredir=allure-results
```

Allure-results можно скачать из завершённого workflow в разделе **Artifacts**.

После скачивания отчёт можно открыть локально:

```
allure serve allure-results
```

---

## Установка и запуск локально

### 1. Клонировать репозиторий с автотестами

```
git clone https://github.com/AmirRoni/SimbirSoft-SDET-Week-2.git
cd SimbirSoft-SDET-Week-2
```

### 2. Создать и активировать виртуальное окружение

Windows:

```
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```
pip install -r requirements.txt
```

### 4. Клонировать тестовый сервис

В отдельную папку рядом с проектом или в любое удобное место:

```
git clone https://github.com/sun6r0/test-service.git
cd test-service
```

### 5. Запустить тестовый сервис

```
docker compose up --build -d
```

После запуска API должен быть доступен по адресу:

```
http://localhost:8080
```

### 6. Запустить автотесты

Из папки проекта с автотестами:

```
pytest
```

Запуск с Allure:

```
pytest --alluredir=allure-results
```

Параллельный запуск:

```
pytest -n 2 --dist=loadgroup
```

Параллельный запуск с Allure:

```
pytest -n 2 --dist=loadgroup --alluredir=allure-results
```

Открыть Allure-отчёт:

```
allure serve allure-results
```

---

## Покрытие по заданию

По заданию требуется создать проект из пяти API-автотестов для всех точек доступа к приложению.

В проекте реализованы 5 положительных API-автотестов:

- `POST /api/create`
- `GET /api/get/{entity_id}`
- `GET /api/getAll`
- `PATCH /api/patch/{entity_id}`
- `DELETE /api/delete/{entity_id}`

Дополнительно реализовано:

- формирование Allure-отчётов
- параллельный запуск тестов через `pytest-xdist`
- запуск тестов в GitHub Actions

---

## Полезные команды

Запуск всех тестов:

```
pytest
```

Запуск конкретного тестового файла:

```
pytest tests/api/test_create_entity.py
```

Запуск с Allure:

```
pytest --alluredir=allure-results
```

Параллельный запуск:

```
pytest -n 2 --dist=loadgroup
```

Параллельный запуск с Allure:

```
pytest -n 2 --dist=loadgroup --alluredir=allure-results
```

Открытие Allure-отчёта:

```
allure serve allure-results
```

Запуск тестового сервиса:

```
docker compose up --build -d
```

Остановка Docker-контейнеров:

```
docker compose down
```

Полный сброс контейнеров и volumes:

```
docker compose down -v
```