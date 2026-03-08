from auction_app.repositories.base_repo import BaseRepo
from ..models import User
from sqlalchemy import select


class UserRepo(BaseRepo):

    async def create_user(self, **user_data):
        new_user = User(**user_data)
        self.db.add(new_user)
        await self.db.flush()
        await self.db.refresh(new_user)
        return new_user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_all_users(self) -> list[User]:
        result = await self.db.execute(select(User))

        return result.scalars().all()

    async def get_user_by_name(self, name: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.name == name)
        )
        return result.scalar_one_or_none()
