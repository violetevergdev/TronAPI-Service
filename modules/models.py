from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from datetime import datetime
from modules.database import Base

class TronInfo(Base):
    __tablename__ = 'tron_info'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    address: Mapped[str] = mapped_column(index=True)
    bandwidth: Mapped[int]
    energy: Mapped[int]
    trx_balance: Mapped[int]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

