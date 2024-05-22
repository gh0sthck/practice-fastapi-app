from pydantic import BaseModel
import pytest

from database import ModelExplorer
from services.categories.models import Category
from services.categories.schemas import CategorySchema

from .conftest import async_session, prepare_database
from .fixtures import create_category

test_model_explorer = ModelExplorer(table=Category, schema=CategorySchema)


@pytest.mark.anyio
@pytest.mark.parametrize("id, name", [(i, f"test_category-{i}") for i in range(10)])
async def test_db_insert(id, name):
    async with async_session() as session:
        result = await test_model_explorer.add(
            schema=CategorySchema(id=id, name=name), session=session
        )
        assert isinstance(result, CategorySchema)


@pytest.mark.anyio
async def test_get_all(categories):
    categories = [CategorySchema.model_validate(cat) for cat in categories]
    async with async_session() as session:
        all_categories = await test_model_explorer.get_all(session=session)
        assert all_categories == categories


@pytest.mark.anyio
@pytest.mark.parametrize("id, name", [(i, f"test_category-{i}") for i in range(10)])
async def test_db_get_id(id, name):
    async with async_session() as session:
        category = await test_model_explorer.get_by_id(id_=id, session=session)
        assert isinstance(category, CategorySchema)
        assert category.name == name
        
