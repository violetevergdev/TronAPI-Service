from datetime import datetime, timezone

from fastapi.concurrency import run_in_threadpool

from app.db.database import Database
from app.services.tron_client import TronCustomClient
from app.db.tron_repo import TronRepo
from app.models.tron_info_model import TronInfo

class TronService:
    def __init__(self, db: Database, api_key: str):
        self.db = db
        self.client = TronCustomClient(api_key)

    async def fetch_and_save_info(self, address: str):
        data = await run_in_threadpool(self.client.get_tron_info, address)

        if not data:
            return None

        async with self.db.get_session() as session:
            repo = TronRepo(session)
            tron_info = TronInfo(
                address=address,
                bandwidth=data['bandwidth'],
                energy=data['energy'],
                trx_balance=data['trx_balance'],
                timestamp=datetime.now(timezone.utc),
            )

            await repo.create(tron_info)
            return tron_info

    async def list_info(self, page: int, per_page: int):
        offset = (page - 1) * per_page

        async with self.db.get_session() as session:
            repo = TronRepo(session)
            total_items = await repo.count()
            items = await repo.get_lst(offset, per_page)
            return total_items, items

