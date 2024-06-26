"""
Database file. 
Don't change nothing.
"""

from typing import List, Optional

from fastapi.responses import Response
import sqlalchemy
import sqlalchemy.exc
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
        result: List = (
            (await session.execute(all_stmt)).scalars().all()
        )
        if result:
            result = [self.schema.model_validate(res.__dict__) for res in result]
        return result

    async def get_by_id(
        self, id_: int, session: AsyncSession
    ) -> Optional[pydantic_schema]:
        """Get only one field by id from table. Table should contain `id` field."""
        specific_stmt = Select(self.table).where(self.table.id == id_)
        result = (await session.execute(specific_stmt)).scalar()
        if result:
            result = self.schema.model_validate(obj=result.__dict__)
        return result

    async def add(
        self, schema: pydantic_schema, session: AsyncSession
    ) -> pydantic_schema:
        """Add new field to table."""
        result = schema
        try:
            add_stmt = Insert(self.table).values(schema.model_dump())
            await session.execute(add_stmt)
        except sqlalchemy.exc.IntegrityError as sql_error:
            result = Response(content=f"{sql_error._message()}", status_code=409)
        else:
            await session.commit()
        finally:
            return result

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
        if await self.get_by_id(id_, session):
            schema = update_schema.model_dump()
            schema["id"] = id_
            schema = update_schema.model_validate(schema)
            result = schema
        else:
            return Response(content="Object not found", status_code=404)
        try:
            update_stmt = (
                Update(self.table)
                .where(self.table.id == id_)
                .values(schema.model_dump())
            )
            await session.execute(update_stmt)
        except sqlalchemy.exc.IntegrityError as sql_error:
            result = Response(content=f"{sql_error._message()}", status_code=409)
        else:
            await session.commit()
        finally:
            return result
