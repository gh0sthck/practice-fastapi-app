from typing import List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .schemas import ProductSchema
from .products import (
    get_all_products,
    get_product_by_id,
    add_product,
)

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/all/")
async def all_products(
    session: AsyncSession = Depends(get_async_session),
) -> List[ProductSchema]:
    products: List[ProductSchema] = await get_all_products(session)
    return products


@products_router.get("/{id}/")
async def specific_product(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[ProductSchema]:
    product: Optional[ProductSchema] = await get_product_by_id(session, id)
    return product


@products_router.post("/new/")
async def new_product(
    product: ProductSchema, session: AsyncSession = Depends(get_async_session)
) -> ProductSchema:
    return await add_product(product, session)
