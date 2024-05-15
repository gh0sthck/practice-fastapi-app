from typing import List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .schemas import ProductSchema
from .products import (
    get_all_products as get_all_prods,
    get_product_by_id as get_prod_id,
    add_product as add_prod,
)

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/all/")
async def get_all_products(
    session: AsyncSession = Depends(get_async_session),
) -> List[ProductSchema]:
    products = await get_all_prods(session)
    return products


@products_router.get("/{id}/")
async def get_product_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[ProductSchema]:
    product: Optional[ProductSchema] = await get_prod_id(session, id)
    return product


@products_router.post("/new/")
async def add_product(
    product: ProductSchema, session: AsyncSession = Depends(get_async_session)
) -> ProductSchema:
    await add_prod(product, session)
    return product
