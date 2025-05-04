from app.services.tron_service import TronService
from app.core.config import Config
from app.db.database import PostgresDatabase

config = Config.get_config()
db = PostgresDatabase(config['database'])

def get_tron_service() -> TronService:
    return TronService(db=db, api_key=config['tron-api']['api-key'])
