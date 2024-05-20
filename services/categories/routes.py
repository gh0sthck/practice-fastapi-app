from typing import List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .categories import (
     add_category, 
     get_all_categories, 
     get_category_by_id
)
from .schemas import CategorySchema


categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("/all/")
async def all_categories(
    session: AsyncSession = Depends(get_async_session),
) -> List[CategorySchema]:
    result: List[CategorySchema] = await get_all_categories(session)
    return result


@categories_router.get("/{id}/")
async def specific_category(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchema]:
    result: Optional[CategorySchema] = await get_category_by_id(id_=id, session=session)
    return result


@categories_router.post("/new/")
async def new_category(
    category: CategorySchema, session: AsyncSession = Depends(get_async_session)
) -> CategorySchema:
    return await add_category(category, session)
