from app.core.config import settings
from app.core.db import engine
from app.users import crud
from app.users.models import User, UserCreate
from sqlmodel import Session, SQLModel, select


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.create_user(session=session, user_create=user_in)
