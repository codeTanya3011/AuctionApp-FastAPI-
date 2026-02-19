from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
from typing import List
from ..schemas import BidCreate, BidOut, LotCreate, LotOut, UserCreate, UserOut
from ..services.auction_service import AuctionService
from ..database.uow import UOWDep
from ..websocket import manager

auction_router = APIRouter(tags=["Auction"])


@auction_router.post("/user", response_model=UserOut)
async def create_user(
    user_data: UserCreate,
    uow: UOWDep
):
    return await AuctionService.create_user(name=user_data.name, uow=uow)


@auction_router.get("/users", response_model=list[UserOut])
async def get_users(
    uow: UOWDep
):
    return await AuctionService.get_all_users(uow=uow)


@auction_router.post("/", response_model=LotOut)
async def create_lot(
    lot_data: LotCreate,
    uow: UOWDep
):
    return await AuctionService.create_lot(lot_data=lot_data, uow=uow)


@auction_router.get("/", response_model=List[LotOut])
async def get_lots(
    uow: UOWDep
):
    return await AuctionService.get_all_active_lots(uow=uow)


@auction_router.post("/{lot_id}/bids", response_model=BidOut)
async def place_bid(
    lot_id: UUID,
    bid_data: BidCreate,
    uow: UOWDep
):
    return await AuctionService.place_bid(
        lot_id=lot_id,
        user_id=bid_data.user_id,
        amount=bid_data.amount,
        uow=uow
    )


@auction_router.websocket("/ws/{lot_id}")
async def websocket_endpoint(websocket: WebSocket, lot_id: UUID):
    await manager.connect(websocket, lot_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, lot_id)
    except Exception:
        manager.disconnect(websocket, lot_id)