from typing import List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import ModelExplorer, get_async_session
from .models import Category
from .schemas import CategorySchema


categories_explorer = ModelExplorer(table=Category, schema=CategorySchema)
categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("/all/")
async def all_categories(
    session: AsyncSession = Depends(get_async_session),
) -> List[CategorySchema]:
    result: List[CategorySchema] = await categories_explorer.get_all(session=session)
    return result


@categories_router.get("/{id}/")
async def specific_category(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchema]:
    result: Optional[CategorySchema] = await categories_explorer.get_by_id(id_=id, session=session)
    return result


@categories_router.post("/new/")
async def new_category(
    category: CategorySchema, session: AsyncSession = Depends(get_async_session)
) -> CategorySchema:
    return await categories_explorer.add(schema=category, session=session)
