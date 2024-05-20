from typing import Optional, List
from unittest import result

from sqlalchemy import Insert, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.categories.schemas import CategorySchema
from .models import Category


async def get_all_categories(session: AsyncSession) -> List[CategorySchema]:
    all_cats = select(Category)
    result: List[CategorySchema] = (await session.execute(all_cats)).scalars().all()
    return result

    
async def get_category_by_id(id_: int, session: AsyncSession) -> Optional[CategorySchema]:
    specific_cat = Select(Category).where(Category.id==id_)
    result: Optional[CategorySchema] = (await session.execute(specific_cat)).scalars().first()
    return result


async def add_category(category: CategorySchema, session: AsyncSession) -> CategorySchema:
    category_to_add = Insert(Category).values(category.model_dump())
    await session.execute(category_to_add)
    await session.commit()
    return category
