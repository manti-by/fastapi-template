import logging

from app.core.config import settings
from app.core.security import get_password_hash
from app.users.models import User
from sqlalchemy import StaticPool, create_engine
from sqlmodel import Session, SQLModel, select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""), poolclass=StaticPool
    )
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
        user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER))
        if not user.first():
            password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
            user = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=password,
                is_superuser=True,
            )
            session.add(user)
            session.commit()


if __name__ == "__main__":
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")
