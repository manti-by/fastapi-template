from typing import Any

from app.core.security import get_password_hash, verify_password
from app.users.models import User, UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_user(
    *, session: AsyncSession, db_user: User, user_in: UserUpdate
) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_users = await session.scalars(statement)
    return session_users.first()


async def authenticate(
    *, session: AsyncSession, email: str, password: str
) -> User | None:
    user = await get_user_by_email(session=session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return
    return user
