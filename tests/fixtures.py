import pytest
from sqlalchemy import Insert

from services.categories.models import Category
from services.products.models import Product
from services.purchases.models import Purchase
from services.sellers.models import Seller
from .conftest import categories, products, purchases, sellers, async_session


@pytest.fixture
async def create_category(categories):
    async with async_session() as session:
        statement = Insert(Category).values(categories)
        await session.execute(statement)
        await session.commit()


@pytest.fixture
async def create_products(products):
    async with async_session() as session:
        statement = Insert(Product).values(products)
        await session.execute(statement)
        await session.commit()


@pytest.fixture
async def create_sellers(sellers):
    async with async_session() as session:
        statement = Insert(Seller).values(sellers)
        await session.execute(statement)
        await session.commit()


@pytest.fixture
async def create_purchases(purchases):
    async with async_session() as session:
        statement = Insert(Purchase).values(purchases)
        await session.execute(statement)
        await session.commit()
