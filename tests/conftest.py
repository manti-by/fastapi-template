import pytest
from app.core.config import settings
from app.core.security import get_password_hash
from app.main import app
from app.users.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from tests import DEFAULT_PASSWORD


@pytest.fixture(name="session")
def session() -> Session:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""), poolclass=StaticPool
    )
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


@pytest.fixture(name="user")
def user(session, faker) -> User:
    password = get_password_hash(DEFAULT_PASSWORD)
    user = User(email=faker.email(), hashed_password=password)
    session.add(user)
    session.commit()
    yield user
