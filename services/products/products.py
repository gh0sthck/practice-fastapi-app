from typing import List, Optional

from sqlalchemy import Insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from .schemas import ProductSchema


async def get_all_products(session: AsyncSession) -> List[ProductSchema]:
    get_all_prods = select(Product)
    results: List[ProductSchema] = (await session.execute(get_all_prods)).scalars().all()
    return [ProductSchema.model_validate(r.__dict__) for r in results]


async def get_product_by_id(session: AsyncSession, id: int) -> Optional[ProductSchema]:
    get_current_prod = select(Product).where(Product.id == id)
    result = (await session.execute(get_current_prod)).scalars().first()
    return ProductSchema.model_validate(result.__dict__) if result else None


async def add_product(product: ProductSchema, session: AsyncSession) -> ProductSchema:
    add_product_stmt = Insert(Product).values(product.model_dump())
    await session.execute(add_product_stmt)
    await session.commit()
    return product
