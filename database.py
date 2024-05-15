"""
Database file. 
Don't change nothing.
"""


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from settings import setting

engine: AsyncEngine = create_async_engine(url=setting.db.dsn)
async_session: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase): ...


async def get_async_session():
    async with async_session() as sess:
        yield sess
