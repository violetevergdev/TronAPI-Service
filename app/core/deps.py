from fastapi import Request

from app.services.tron_service import TronService


async def get_tron_service(request: Request) -> TronService:
    db = request.app.state.db
    config = request.app.state.config
    redis = request.app.state.redis

    return TronService(db=db, api_key=config["tron-api"]["api-key"], redis=redis)
