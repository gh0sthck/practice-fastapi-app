from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import ModelExplorer, get_async_session
from services.sellers.models import Seller
from services.sellers.schemas import SellerSchema, SellerUpdateSchema


sellers_explorer = ModelExplorer(table=Seller, schema=SellerSchema)
sellers_router = APIRouter(prefix="/sellers", tags=["Sellers"])


@sellers_router.get("/all/")
async def all_sellers(
    session: AsyncSession = Depends(get_async_session),
) -> List[SellerSchema]:
    return await sellers_explorer.get_all(session=session)


@sellers_router.get("/{id}/")
async def specific_seller(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[SellerSchema]:
    return await sellers_explorer.get_by_id(id_=id, session=session)


@sellers_router.post("/new/")
async def all_sellers(
    seller: SellerSchema,
    session: AsyncSession = Depends(get_async_session),
) -> SellerSchema:
    return await sellers_explorer.add(schema=seller, session=session)


@sellers_router.delete("/{id}/")
async def seller_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[SellerSchema]:
    return await sellers_explorer.delete_by_id(id_=id, session=session)


@sellers_router.put("/update/")
async def seller_update(
    id: int, seller: SellerUpdateSchema, session: AsyncSession = Depends(get_async_session)
) -> SellerUpdateSchema:
    return await sellers_explorer.update(id_=id, update_schema=seller, session=session)
