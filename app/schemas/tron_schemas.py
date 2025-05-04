from typing import List

from pydantic import BaseModel
from datetime import datetime


class TronRequest(BaseModel):
    address: str


class TronItemResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    trx_balance: int
    timestamp: datetime


class TronResponse(BaseModel):
    total_items: int
    total_pages: int
    page: int
    per_page: int
    items: List[TronItemResponse]

