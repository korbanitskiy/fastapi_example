from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.user.models import UserEntity
from app.settings import AppSettings


class UserRepository:
    def __init__(self, settings: AppSettings, session: AsyncSession):
        self.settings = settings
        self.session = session

    async def get_all(self) -> Sequence[UserEntity]:
        result = await self.session.execute(select(UserEntity))
        return result.scalars().all()

    async def select_user(self, user_id: int) -> UserEntity | None:
        qs = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session.execute(qs)
        return result.scalar_one_or_none()

    async def set_user_as_admin(self, user_id) -> None:
        qs = update(UserEntity).where(UserEntity.id == user_id).values(is_admin=True)
        await self.session.execute(qs)
