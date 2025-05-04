from fastapi import APIRouter, HTTPException, Depends

from app.schemas.tron_schemas import TronRequest, TronItemResponse, TronResponse
from app.services.tron_service import TronService
from app.core.deps import get_tron_service

router = APIRouter()

@router.post("/tron-info/", response_model=TronItemResponse)
async def create_info(request: TronRequest, service: TronService = Depends(get_tron_service)):
    info = await service.fetch_and_save_info(request.address)

    if not info:
        raise HTTPException(status_code=404, detail='Address not found')

    return TronItemResponse(
        address=info.address,
        bandwidth=info.bandwidth,
        energy=info.energy,
        trx_balance=info.trx_balance,
        timestamp=info.timestamp,
    )

@router.get('/tron-info/', response_model=TronResponse)
async def get_info(service: TronService = Depends(get_tron_service), page: int = 1, per_page: int = 10):
    total_items, items = await service.list_info(page, per_page)

    return TronResponse(
        total_items=total_items,
        total_pages=(total_items + per_page - 1) // per_page,
        page=page,
        per_page=per_page,
        items=[TronItemResponse(
            address=el.address,
            bandwidth=el.bandwidth,
            energy=el.energy,
            trx_balance=el.trx_balance,
            timestamp=el.timestamp,
        ) for el in items]
    )

