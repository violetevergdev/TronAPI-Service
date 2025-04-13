import math
import os
import datetime
from typing import Dict, Any, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

import modules.models as models
import modules.schemas as schemas
from modules.common.load_config import Configuration
from modules.database import Database
from modules.tron_client import TronCustomClient

app = FastAPI()


class TronService:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        if os.getenv('ENV') == 'test':
            self.database = Database(config=self.config['database']['postgres_test'])
        else:
            self.database = Database(config=self.config['database']['postgres'])
        self._init_table()

    def _init_table(self) -> None:
        try:
            models.Base.metadata.create_all(bind=self.database.engine)
        except Exception as e:
            raise RuntimeError(f"Database init error: {e}")

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def get_db_session(self) -> Generator[Session, None, None]:
        yield from self.database.get_session()


configuration = Configuration.get_config()
tron_service = TronService(configuration)


@app.post("/tron-info/", response_model=schemas.TronItemResponse)
def post_tron_info(
        request: schemas.TronRequest,
        db: Session = Depends(tron_service.get_db_session)
):
    tron_client = TronCustomClient(configuration)
    data = tron_client.get_tron_info(request.address)
    if data:
        try:
            tron_info = models.TronInfo(
                address=request.address,
                bandwidth=data['bandwidth'],
                energy=data['energy'],
                trx_balance=data['trx_balance'],
                timestamp=datetime.datetime.now(datetime.UTC).isoformat(sep=' ', timespec='seconds'),
            )
            db.add(tron_info)
            db.commit()
            db.refresh(tron_info)

            return {
                "address": tron_info.address,
                "bandwidth": tron_info.bandwidth,
                "energy": tron_info.energy,
                "trx_balance": tron_info.trx_balance,
                "timestamp": tron_info.timestamp.isoformat(sep=' ', timespec='seconds'),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server Error: {e}")

    else:
        raise HTTPException(status_code=404, detail=f"Tron info not found: {request}")


@app.get("/tron-info/", response_model=schemas.TronResponse)
def get_info(
        db: Session = Depends(tron_service.get_db_session),
        page: int = 1,
        per_page: int = 10
):
    try:
        total_data = db.query(models.TronInfo).count()
        offset = (page - 1) * per_page

        items = db.query(models.TronInfo) \
            .order_by(models.TronInfo.id.desc()) \
            .offset(offset) \
            .limit(per_page) \
            .all()

        items_dict = [item.__dict__ for item in items]

        for item in items_dict:
            item.pop('_sa_instance_state', None)

        total_pages = math.ceil(total_data / per_page) \
            if per_page > 0 else 1

        return {
            "items": items_dict,
            "pagination": {
                "total_items": total_data,
                "total_pages": total_pages,
                "page": page,
                "per_page": per_page,
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
