from typing import List, Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import ModelExplorer, get_async_session
from .models import Product
from .schemas import ProductSchema, ProductUpdateSchema

product_explorer = ModelExplorer(table=Product, schema=ProductSchema)
products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/all/")
async def all_products(
    session: AsyncSession = Depends(get_async_session),
) -> List[ProductSchema]:
    return await product_explorer.get_all(session=session)


@products_router.get("/{id}/")
async def specific_product(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[ProductSchema]:
    return await product_explorer.get_by_id(id_=id, session=session)


@products_router.post("/new/")
async def new_product(
    product: ProductSchema, session: AsyncSession = Depends(get_async_session)
) -> ProductSchema | dict[str, str]:
    return await product_explorer.add(schema=product, session=session)


@products_router.delete("/{id}/")
async def product_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[ProductSchema]:
    return await product_explorer.delete_by_id(id_=id, session=session)


@products_router.put("/update/")
async def product_update(
    id: int, product: ProductUpdateSchema, session: AsyncSession = Depends(get_async_session)
) -> Optional[ProductUpdateSchema]:
    return await product_explorer.update(id_=id, update_schema=product, session=session)
