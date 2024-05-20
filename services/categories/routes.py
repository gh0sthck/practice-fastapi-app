from typing import List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import ModelExplorer, get_async_session
from .models import Category
from .schemas import CategorySchema, CategoryUpdateSchema


categories_explorer = ModelExplorer(table=Category, schema=CategorySchema)
categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("/all/")
async def all_categories(
    session: AsyncSession = Depends(get_async_session),
) -> List[CategorySchema]:
    return await categories_explorer.get_all(session=session)


@categories_router.get("/{id}/")
async def specific_category(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchema]:
    return await categories_explorer.get_by_id(id_=id, session=session)


@categories_router.post("/new/")
async def new_category(
    category: CategorySchema, session: AsyncSession = Depends(get_async_session)
) -> CategorySchema:
    return await categories_explorer.add(schema=category, session=session)


@categories_router.delete("/{id}/")
async def category_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchema]:
    return await categories_explorer.delete_by_id(id_=id, session=session)


@categories_router.put("/update/")
async def category_update(
    id: int,
    category: CategoryUpdateSchema,
    session: AsyncSession = Depends(get_async_session)
) -> CategorySchema:
    return await categories_explorer.update(id_=id, schema=category, session=session)
