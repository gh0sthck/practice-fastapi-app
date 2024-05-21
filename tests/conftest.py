"""
Unit-test configuration file.
"""
import datetime
from typing import List

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)

from main import app
from settings import setting
from database import Base, get_async_session

test_engine: AsyncEngine = create_async_engine(url=setting.tests.db.dsn)
async_session: AsyncSession = async_sessionmaker(
    bind=test_engine, expire_on_commit=False
)
Base.metadata.bind = test_engine


async def get_override_async_session():
    async with async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = get_override_async_session


@pytest.fixture(scope="session")
def anyio_backend():
    """DON'T TOUCH THIS! Need to tests and prepare database work."""
    return 'asyncio'


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def categories() -> List[dict]:
    return [
        {
            "id": i,
            "name": f"test_category-{i}",
        }
        for i in range(10)
    ]


@pytest.fixture
def products() -> List[dict]:
    return [
        {
            'id': i, 
            'name': f'test_product-{i}', 
            'count': i*2, 
            'cost': i*3, 
            'category_id': i
        }
        for i in range(10)
    ]
    
    
@pytest.fixture
def sellers() -> List[dict]:
    return [
        {
            "id": i,
            "first_name": f"first_name-{i}",
            "last_name": f"last_name-{i}",
            "sallary": 60000,
            "phone": f"{i} {i}{i+2}{i+3} {i+4}{i+5}{i+6}-{i*2}{i*3}-{i/2}{i/3}",
            "is_personal": False,
            "birthday": datetime.datetime.now()
        }
        for i in range(10)
    ]


@pytest.fixture
def purchases() -> List[dict]:
    return [
        {
            "id": i,
            "date": datetime.datetime.now(),
            "update_date": datetime.datetime.now(),
            "seller_id": i,
        }
        for i in range(10)
    ]
