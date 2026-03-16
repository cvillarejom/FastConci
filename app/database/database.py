from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.database_user,
    password=settings.database_password,
    host=settings.database_url,
    database=settings.database_name,
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session




