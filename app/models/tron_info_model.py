from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime
from datetime import datetime, timezone
from app.db.base import Base


class TronInfo(Base):
    __tablename__ = 'tron_info'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    address: Mapped[str] = mapped_column(index=True)
    bandwidth: Mapped[int]
    energy: Mapped[int]
    trx_balance: Mapped[int]
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), index=True)

    def to_dict(self):
        return {
            "address": self.address,
            "bandwidth": self.bandwidth,
            "energy": self.energy,
            "trx_balance": self.trx_balance,
            "timestamp": self.timestamp.isoformat(),
        }
