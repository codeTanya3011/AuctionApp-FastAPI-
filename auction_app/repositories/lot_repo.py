from ..core import LotStatus
from ..repositories import BaseRepo
from sqlalchemy.future import select
from ..models.lot import Lot
from uuid import UUID


class LotRepo(BaseRepo):

    async def create_lot(self, **lot_data) -> Lot:
        new_lot = Lot(**lot_data)
        self.db.add(new_lot)
        return new_lot

    async def get_active_lots(self):
        result = await self.db.execute(
            select(Lot).where(Lot.status == "running")
        )
        return result.scalars().all()

    async def get_lot_by_id(self, lot_id: UUID):
        return await self.db.get(Lot, lot_id)

    async def update_lot_status(self, lot_id: UUID, status: LotStatus):
        lot = await self.get_lot_by_id(lot_id)
        if lot:
            lot.status = status


