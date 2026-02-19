from ..repositories import BaseRepo
from ..models import Bid
from sqlalchemy import select
from uuid import UUID


class BidRepo(BaseRepo):

    async def create_bid(self, **bid_data):
        new_bid = Bid(**bid_data)
        self.db.add(new_bid)
        return new_bid

    async def get_bets_for_lot(self, lot_id: UUID):
        result = await self.db.execute(
            select(Bid).where(Bid.lot_id == lot_id).order_by(Bid.created_at.desc())
        )
        return result.scalars().all()

    async def get_bets_for_user(self, user_id: int):
        result = await self.db.execute(
            select(Bid).where(Bid.user_id == user_id).order_by(Bid.created_at.desc())
        )
        return result.scalars().all()

