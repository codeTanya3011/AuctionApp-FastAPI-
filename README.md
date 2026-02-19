# Auction Real-Time Service

Асинхронный сервис аукциона на FastAPI с поддержкой WebSocket и Unit of Work.

## Технологии
* **FastAPI** — веб-фреймворк
* **SQLAlchemy 2.0 (Async)** — работа с БД
* **PostgreSQL** — основное хранилище
* **Pydantic v2** — валидация данных
* **WebSockets** — уведомления о ставках в реальном времени

## Как запустить

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Склонируйте репозиторий.

3. Запустите проект командой:
   ```bash
   docker-compose up --build
   
4. Сервис будет доступен по адресу: http://localhost:8080

5. Документация API (Swagger): http://localhost:8080/docs

## Как протестировать WebSocket

Для проверки обновлений в реальном времени:

1. Откройте любой WebSocket-клиент (например, расширение в Chrome или PieSocket).

2. Подключитесь к: ws://localhost:8080/api/v4/lots/ws/{lot_id}

3. Сделайте POST запрос на создание ставки через Swagger.

4. Вы увидите мгновенное уведомление в WebSocket-клиенте.