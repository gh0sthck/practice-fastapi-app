import pytest
from sqlalchemy import Delete, Insert

from services.categories.models import Category
from services.products.models import Product
from services.purchases.models import Purchase
from services.sellers.models import Seller
from .conftest import categories, products, purchases, sellers, async_session


@pytest.fixture()
async def create_category(categories):
    async with async_session() as session:
        await session.execute(Delete(Category))
        await session.commit()
        statement = Insert(Category).values(categories)
        await session.execute(statement)
        await session.commit()
    yield
    async with async_session() as session:
        await session.execute(Delete(Category))
        await session.commit()


@pytest.fixture
async def create_products(create_category, products):
    async with async_session() as session:
        await session.execute(Delete(Product))
        await session.commit()
        statement = Insert(Product).values(products)
        await session.execute(statement)
        await session.commit()
    yield
    async with async_session() as session:
        await session.execute(Delete(Product))
        await session.commit()


@pytest.fixture
async def create_sellers(sellers):
    async with async_session() as session:
        await session.execute(Delete(Seller))
        await session.commit()
        statement = Insert(Seller).values(sellers)
        await session.execute(statement)
        await session.commit()
    yield
    async with async_session() as session:
        await session.execute(Delete(Seller))
        await session.commit()


@pytest.fixture
async def create_purchases(create_products, purchases):
    async with async_session() as session:
        await session.execute(Delete(Purchase))
        await session.commit()
        statement = Insert(Purchase).values(purchases)
        await session.execute(statement)
        await session.commit()
    yield
    async with async_session() as session:
        await session.execute(Delete(Purchase))
        await session.commit()
