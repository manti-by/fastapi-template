import pytest
from app.core.config import settings
from app.main import app
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture(name="session")
def session() -> Session:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client() -> TestClient:
    with TestClient(app) as client:
        yield client
