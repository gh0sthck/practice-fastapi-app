"""
Database file. 
Don't change nothing.
"""

from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Delete, Select, Insert, Update
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from pydantic import BaseModel as pydantic_schema

from settings import setting

engine: AsyncEngine = create_async_engine(url=setting.db.dsn)
async_session: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session():
    async with async_session() as sess:
        yield sess


class Base(DeclarativeBase): ...


class ModelExplorer:
    """
    CRUD ORM operations.
    """

    def __init__(self, table: Base, schema: pydantic_schema) -> None:
        self.table: Base = table
        self.schema: pydantic_schema = schema

    async def clear_table(self, session: AsyncSession) -> None:
        clear_stmt = Delete(self.table)
        await session.execute(clear_stmt)
        await session.commit()

    async def get_all(self, session: AsyncSession) -> List[pydantic_schema]:
        """Get all fields from table."""
        all_stmt = Select(self.table)
        result: List[self.schema] = (await session.execute(all_stmt)).scalars().all()
        return result

    async def get_by_id(
        self, id_: int, session: AsyncSession
    ) -> Optional[pydantic_schema]:
        """Get only one field by id from table. Table should contain `id` field."""
        specific_stmt = Select(self.table).where(self.table.id == id_)
        result: Optional[self.pydantic_schema] = (
            (await session.execute(specific_stmt)).scalars().first()
        )
        return result

    async def add(
        self, schema: pydantic_schema, session: AsyncSession
    ) -> pydantic_schema:
        """Add new field to table."""
        add_stmt = Insert(self.table).values(schema.model_dump())
        await session.execute(add_stmt)
        await session.commit()
        return schema

    async def delete_by_id(
        self, id_: int, session: AsyncSession
    ) -> Optional[pydantic_schema]:
        """Delete one field by id from table. Table should contain `id` field."""
        field: Optional[Base] = await self.get_by_id(id_=id_, session=session)
        if field:
            delete_field = Delete(self.table).where(self.table.id == id_)
            await session.execute(delete_field)
            await session.commit()
            return field
        return None

    async def update(
        self, id_: int, update_schema: pydantic_schema, session: AsyncSession
    ) -> pydantic_schema:
        """Update field. Field should contain id field and have update schema."""
        schema = update_schema.model_dump()
        schema["id"] = id_

        schema = self.schema.model_validate(schema)

        update_stmt = (
            Update(self.table).where(self.table.id == id_).values(schema.model_dump())
        )

        await session.execute(update_stmt)
        await session.commit()

        return schema
