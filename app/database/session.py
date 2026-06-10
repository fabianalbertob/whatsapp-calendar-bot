from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config.settings import settings
from app.database.base import Base

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session