from datetime import datetime, timezone
import json
from typing import Optional, Dict, Any

from fastapi.concurrency import run_in_threadpool
from redis.asyncio import Redis

from app.db.database import Database
from app.services.tron_client import TronCustomClient
from app.db.tron_repo import TronRepo
from app.models.tron_info_model import TronInfo


class TronService:
    def __init__(self, db: Database, api_key: str, redis: Optional[Redis] = None):
        self.db = db
        self.client = TronCustomClient(api_key)
        self.redis = redis

    async def fetch_and_save_info(self, address: str):
        cache_key = f"tron:addr:{address}"
        if self.redis:
            cached_data = await self._fetch_from_cache(cache_key)
            if cached_data:
                return TronInfo(
                    address=cached_data["address"],
                    bandwidth=cached_data["bandwidth"],
                    energy=cached_data["energy"],
                    trx_balance=cached_data["trx_balance"],
                    timestamp=datetime.fromisoformat(cached_data["timestamp"]),
                )

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
            if self.redis:
                await self.redis.setex(cache_key, 120, json.dumps(tron_info.to_dict()))
                await self._invalid_list_cache()

            return tron_info

    async def list_info(self, page: int, per_page: int):
        cached_key = f"tron:list:page-{page}:per_page-{per_page}"

        if self.redis:
            cached_data = await self._fetch_from_cache(cached_key)
            if cached_data:
                total = cached_data["total"]
                items = [
                    TronInfo(
                        address=item["address"],
                        bandwidth=item["bandwidth"],
                        energy=item["energy"],
                        trx_balance=item["trx_balance"],
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                    )
                    for item in cached_data["items"]
                ]

                return total, items

        offset = (page - 1) * per_page

        async with self.db.get_session() as session:
            repo = TronRepo(session)
            total_items = await repo.count()
            items = await repo.get_lst(offset, per_page)

            if self.redis:
                items_dict = [item.to_dict() for item in items]
                data_to_cache = {
                    "total": total_items,
                    "items": items_dict,
                }
                await self.redis.setex(cached_key, 3600, json.dumps(data_to_cache))

            return total_items, items

    async def _fetch_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

    async def _invalid_list_cache(self) -> None:
        keys = await self.redis.keys("tron:list:*")
        if keys:
            await self.redis.delete(*keys)
