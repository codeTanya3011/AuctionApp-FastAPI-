import pytest
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from main import app


@pytest.mark.asyncio
async def test_create_user(client):
    name = f"Alice_{uuid4().hex[:4]}"
    response = await client.post("/api/v4/lots/user", json={"name": name})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user_duplicate(client):
    name = f"Duplicate_{uuid4().hex[:4]}"

    await client.post("/api/v4/lots/user", json={"name": name})
    response = await client.post("/api/v4/lots/user", json={"name": name})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_place_bid_lot_not_found(client, create_user):
    user = await create_user(name=f"Test UserCheapskate_{uuid4().hex[:4]}")
    fake_id = str(uuid4())

    bid_data = {"user_id": int(user.id), "amount": "200.00"}
    response = await client.post(f"/api/v4/lots/{fake_id}/bids", json=bid_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Лот не знайдено"


@pytest.mark.asyncio
async def test_place_bid_success(client, create_lot, create_user):
    lot = await create_lot(title="Test Lot", price="100.00")
    user = await create_user(name=f"User_{uuid4().hex[:4]}")

    bid_data = {"user_id": int(user.id), "amount": "150.00"}

    response = await client.post(f"/api/v4/lots/{str(lot.id)}/bids", json=bid_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_place_bid_too_low(client, create_lot, create_user):
    lot = await create_lot(title="Test Lot", price="100.00")
    user = await create_user(name=f"User_{uuid4().hex[:4]}")

    bid_data = {"user_id": int(user.id), "amount": "90.00"}
    response = await client.post(f"/api/v4/lots/{str(lot.id)}/bids", json=bid_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Ставка повинна бути вищою за поточну ціну"


@pytest.mark.asyncio
async def test_websocket_broadcast(client: AsyncClient):
    user_name = f"WS_User_{uuid4().hex[:4]}"
    u_res = await client.post("/api/v4/lots/user", json={"name": user_name})
    assert u_res.status_code == 200
    user_id = u_res.json()["id"]

    end_time = (datetime.now(timezone.utc) + timedelta(days=1)).replace(tzinfo=None).isoformat()
    l_res = await client.post("/api/v4/lots/", json={
        "title": "WS Lot",
        "description": "test websocket",
        "start_price": "100.00",
        "end_time": end_time
    })
    assert l_res.status_code == 200
    lot_id = l_res.json()["id"]

    path = f"/api/v4/lots/ws/{lot_id}"

    with TestClient(app, raise_server_exceptions=True) as sync_client:
        try:

            with sync_client.websocket_connect(path) as ws:

                bid_data = {
                    "user_id": int(user_id),
                    "amount": "150.00"
                }
                bid_res = await client.post(f"/api/v4/lots/{lot_id}/bids", json=bid_data)
                assert bid_res.status_code == 200

                message = ws.receive_json()

                assert message["type"] == "bid_placed"
                assert message["lot_id"] == str(lot_id)
                assert float(message["amount"]) == 150.00

        except WebSocketDisconnect as e:
            pytest.fail(f"WebSocket закрився надто рано. Код: {e.code}")
        except Exception as e:
            pytest.fail(f"Помилка в тесте WebSocket: {type(e).__name__}: {e}")