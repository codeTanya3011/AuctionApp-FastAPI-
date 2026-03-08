# 🔨 Auction Real-Time Service

An asynchronous auction platform built with **FastAPI**, featuring **WebSockets**
for real-time bid updates and the **Unit of Work** architectural pattern.

---

### 🚀 Technologies & Stack
* **FastAPI** — High-performance Python web framework.
* **SQLAlchemy 2.0 (Async)** — Professional async toolkit and ORM.
* **PostgreSQL** — Robust relational database.
* **Pydantic v2** — Modern data validation and settings.
* **WebSockets** — Live bid notifications for all participants.
* **Docker & Compose** — Full containerization for easy deployment.

---

### ✨ Core Features
* **🔄 Unit of Work Pattern**: Implements atomic transactions to ensure data integrity across the database.
* **🛡️ Robust Error Handling**: 
    - **Custom Domain Exceptions**: Specialized classes for **Bid**, **User**, and **Lot** logic.
    - **Global Registry**: Centralized exception handlers that return consistent, user-friendly JSON responses.
* **⚡ Real-Time Events**: Immediate notifications sent via WebSockets whenever a new bid is placed.

---

### 🧪 Testing & Quality
The project includes automated tests using `pytest` and `asyncpg`. 

> **Note:** Tests require a separate database named `test3_db`. You can create it manually inside the running container before running tests:

1. **Create the test database**:
   ```bash
   docker-compose exec db_container3 psql -U postgres -c "CREATE DATABASE test3_db;"
2. **Run Tests**:
    ```bash
    docker-compose exec api pytest -v
    ```
---

### 🛠️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Launch via Docker**:
    ```bash
    docker-compose up --build -d
    ```

3.  **Explore the API**:
    - **Base URL**: `http://localhost:8080`
    - **Swagger UI**: `http://localhost:8080/docs`
---

### 🕹️ Core Auction Flow (How to Test)
To see the real-time bidding in action, follow this sequence:

1.  **Create a User**: 
    Use `POST /api/v4/lots/user` to create a participant. Copy the `user_id`.
2.  **Create a Lot**: 
    Use `POST /api/v4/lots/` to create an auction item. Copy the `lot_id` (UUID).
3.  **Open WebSocket Connections**:
    Open **two or more** tabs in your WebSocket client (e.g., Postman or PieSocket) and connect to:
    `ws://localhost:8080/api/v4/lots/ws/{lot_id}`
4. **Place a Bid**:
    Go to Swagger and make a `POST /api/v4/lots/{lot_id}/bids` request with a user ID and bid amount.
5. **Observe Real-Time Broadcast**:
    Check your WebSocket tabs — you will see the bid notification arrive **simultaneously** in all connected clients. 🚀
---

### 📡 API Overview
While full documentation is available via Swagger, here are the key functional areas:
* **Users**: Create and manage auction participants.
* **Lots**: List active auctions or create new items.
* **Bidding**: Place bids and track history.
* **Real-Time**: WebSocket-based broadcast system for instant price updates.
