from datetime import datetime, timezone
from decimal import Decimal
from ..core import LotStatus
from ..exceptions import AuctionException
from ..websocket import manager
from ..schemas import LotCreate
from ..database.uow import UnitOfWork
from uuid import UUID as PyUUID


class AuctionService:

    @staticmethod
    async def create_user(name: str, uow: UnitOfWork):
        async with uow:
            existing_user = await uow.users.get_user_by_name(name)

            if existing_user:
                raise AuctionException(status_code=400, detail="Користувач із таким ім'ям вже існує")

            new_user = await uow.users.create_user(name=name)
            await uow.commit()
            return new_user

    @staticmethod
    async def get_all_users(uow: UnitOfWork):
        async with uow:
            users = await uow.users.get_all_users()
            return users

    @staticmethod
    async def create_lot(lot_data: LotCreate, uow: UnitOfWork):
        async with uow:
            if lot_data.end_time.tzinfo is not None:
                lot_data.end_time = lot_data.end_time.replace(tzinfo=None)

            if lot_data.end_time < datetime.now(timezone.utc).replace(tzinfo=None):
                raise AuctionException(detail="Час закінчення має бути у майбутньому")

            data_dict = lot_data.model_dump()

            if data_dict.get("current_price") is None:
                data_dict["current_price"] = data_dict["start_price"]

            new_lot = await uow.lots.create_lot(**data_dict)
            await uow.commit()
            return new_lot

    @staticmethod
    async def get_lot_details(lot_id: PyUUID, uow: UnitOfWork):
        async with uow:
            if isinstance(lot_id, str):
                try:
                    lot_id = PyUUID(lot_id)
                except ValueError:
                    raise AuctionException(status_code=400, detail="Некоректний формат ID")

            lot = await uow.lots.get_lot_by_id(lot_id)

            if not lot:
                raise AuctionException(status_code=404, detail="Лот не знайдено")
            return lot

    @staticmethod
    async def get_all_active_lots(uow: UnitOfWork):
        async with uow:
            lots = await uow.lots.get_active_lots()
            return lots

    @staticmethod
    async def place_bid(lot_id: PyUUID, user_id: int, amount: Decimal, uow: UnitOfWork):
        if isinstance(lot_id, str):
            lot_id = PyUUID(lot_id)

        async with uow:
            lot = await uow.lots.get_lot_by_id(lot_id)
            user = await uow.users.get_user_by_id(user_id)

            if not lot:
                raise AuctionException(status_code=404, detail="Лот не знайдено")
            if not user:
                raise AuctionException(status_code=404, detail="Користувача не знайдено")

            if amount <= lot.current_price:
                raise AuctionException(status_code=400, detail="Ставка повинна бути вищою за поточну ціну")

            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if lot.status == LotStatus.ended or (lot.end_time and lot.end_time < now):
                raise AuctionException(status_code=400, detail="Аукціон вже завершено")

            lot.current_price = amount
            new_bid = await uow.bids.create_bid(lot_id=lot_id, user_id=user_id, amount=amount)
            await uow.commit()

            notification = {
                "type": "bid_placed",
                "lot_id": str(lot_id),
                "bidder": user.name,
                "amount": float(amount)
            }
            await manager.broadcast(lot_id, notification)  #ws
            return new_bid