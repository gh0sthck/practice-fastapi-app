from typing import Iterable

import pytest
from sqlalchemy import Delete, Insert
from sqlalchemy.orm import DeclarativeBase

from services.categories.models import Category
from services.products.models import Product
from services.purchases.models import Purchase
from services.sellers.models import Seller
from .conftest import categories, products, purchases, sellers, async_session


async def prepare(table: DeclarativeBase, values: Iterable):
    async with async_session() as session:
        await session.execute(Delete(table))
        await session.commit()
        statement = Insert(table).values(values)
        await session.execute(statement)
        await session.commit()
    

@pytest.fixture()
async def create_category(categories):
    await prepare(Category, categories)
    yield
    async with async_session() as session:
        await session.execute(Delete(Category))
        await session.commit()


@pytest.fixture
async def create_products(create_category, products):
    await prepare(Product, products)
    yield
    async with async_session() as session:
        await session.execute(Delete(Product))
        await session.commit()


@pytest.fixture
async def create_sellers(sellers):
    await prepare(Seller, sellers)
    yield
    async with async_session() as session:
        await session.execute(Delete(Seller))
        await session.commit()


@pytest.fixture
async def create_purchases(create_products, purchases):
    await prepare(Purchase, purchases)
    yield
    async with async_session() as session:
        await session.execute(Delete(Purchase))
        await session.commit()
