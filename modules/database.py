from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session


class Database:
    def __init__(self, config):
        self.config = config
        self.DB_URL = self.create_url()
        self.engine = create_engine(self.DB_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.config['user']}:{self.config['password']}@"
            f"{self.config['host']}:{self.config['port']}/"
            f"{self.config['database']}"
        )

    def get_session(self) -> Generator[Session, None, None]:
        session: Session = self.SessionLocal()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()



class Base(DeclarativeBase):
    pass
