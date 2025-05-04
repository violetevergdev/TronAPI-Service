from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.tron_info_model import TronInfo

class TronRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TronInfo) -> None:
        self.session.add(data)

    async def count(self) -> int:
        res = await self.session.scalar(select(func.count()).select_from(TronInfo))
        return res

    async def get_lst(self, offset: int, limit: int) -> List[TronInfo]:
        res = await self.session.execute(
            select(TronInfo)
            .order_by(TronInfo.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return res.scalars().all()


