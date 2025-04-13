import os
import pytest
from fastapi.testclient import TestClient
from typing import Generator
from sqlalchemy.orm import Session

from modules.common.load_config import Configuration
from modules.database import Database, Base
from main import app, TronService, tron_service


@pytest.fixture(autouse=True, scope='session')
def _set_test_env():
    os.environ['ENV'] = 'test'
    yield
    os.environ.pop('ENV', None)


@pytest.fixture(scope='session')
def _setup_db():
    config = Configuration.get_config()['database']['postgres_test']
    test_database = Database(config)

    Base.metadata.drop_all(bind=test_database.engine)
    Base.metadata.create_all(bind=test_database.engine)

    yield test_database

    test_database.engine.dispose()


@pytest.fixture
def db_session(_setup_db) -> Generator[Session, None, None]:
    session = next(_setup_db.get_session())
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope='class')
def _setup_api() -> Generator[str, Configuration, TronService]:
    TEST_URL = "/tron-info/"
    config = Configuration().get_config()
    test_tron_service = TronService(config)

    yield TEST_URL, config, test_tron_service


@pytest.fixture(scope='class')
def test_client(_setup_api) -> Generator[TestClient, None, None]:
    _, _, test_tron_service = _setup_api
    orig_dep = tron_service.get_db_session

    app.dependency_overrides[orig_dep] = test_tron_service.get_db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
