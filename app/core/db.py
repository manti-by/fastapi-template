from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
