from typing import List, Optional

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import ModelExplorer, get_async_session
from services.purchases.models import Purchase
from services.purchases.schemas import PurchaseAddSchema, PurchaseSchema

purchases_explorer = ModelExplorer(table=Purchase, schema=PurchaseSchema)
purchases_router = APIRouter(prefix="/purchases", tags=["Purchases"])


@purchases_router.get("/all/")
async def all_purchases(
    session: AsyncSession = Depends(get_async_session),
) -> List[PurchaseSchema]:
    result: List[PurchaseSchema] = await purchases_explorer.get_all(session=session)
    return result


@purchases_router.get("/{id}/")
async def specific_purchase(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[PurchaseSchema]:
    result: Optional[PurchaseSchema] = await purchases_explorer.get_by_id(
        id_=id, session=session
    )
    return result


@purchases_router.post("/new/")
async def new_purchase(
    purchase: PurchaseAddSchema,
    session: AsyncSession = Depends(get_async_session)
) -> PurchaseAddSchema:
    return await purchases_explorer.add(schema=purchase, session=session)
