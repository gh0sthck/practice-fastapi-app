import datetime

import httpx
import pytest

from main import app
from settings import setting
from .fixtures import create_category, create_products, create_purchases, create_sellers


@pytest.mark.anyio
async def test_app_docs():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=setting.tests.base_url
    ) as client:
        docs = await client.get(setting.docs_url)

        assert "<!DOCTYPE html>" in docs.content.decode()
        assert docs.status_code == 200


@pytest.mark.anyio
async def test_categories(create_category, categories):
    category_to_add = {
        "id": 12345,
        "name": f"test_category-added",
    }

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=setting.tests.base_url
    ) as client:
        # get
        cats = await client.get("/categories/all/")

        assert cats.status_code == 200
        assert cats.json() == categories

        # post
        cats_post = await client.post("/categories/new/", json=category_to_add)
        added_cat = await client.get(f"/categories/{category_to_add['id']}/")

        assert cats_post.status_code == 200
        assert category_to_add == added_cat.json()


@pytest.mark.anyio
async def test_products(create_products, products):
    product_to_add = {
        "id": 12345,
        "name": "test_product-added",
        "count": 123,
        "cost": 123,
        "category_id": 0,
    }

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=setting.tests.base_url
    ) as client:
        # get
        prods = await client.get("/products/all/")

        assert prods.status_code == 200
        assert prods.json() == products

        # post
        add_product = await client.post("/products/new/", json=product_to_add)
        added_product = await client.get(f"/products/{product_to_add['id']}/")

        assert add_product.status_code == 200
        assert product_to_add == added_product.json()


@pytest.mark.anyio
async def test_sellers_and_purchases(
    create_sellers, create_purchases, sellers, purchases
):
    seller_to_add = {
        "id": 12345,
        "first_name": "first_name-added",
        "last_name": f"last_name-added",
        "sallary": 60000,
        "phone": f"1 234 567 89-90",
        "is_personal": False,
        "birthday": datetime.datetime.date(datetime.datetime.now()).strftime(format="%Y-%m-%d"),
    }
    
    purchase_to_add = {
        "id": 12345,
        "seller_id": 12345,
    }

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=setting.tests.base_url
    ) as client:
        # get
        sells = await client.get("/sellers/all/")
        purchs = await client.get("/purchases/all/")

        assert sells.status_code == 200

        for sell in sellers:
            sell["birthday"] = datetime.datetime.date(sell["birthday"]).strftime(
                format="%Y-%m-%d"
            )
            assert sell in sells.json()

        assert purchs.status_code == 200

        for purchase in purchs.json():
            purchase["date"] = datetime.datetime.fromisoformat(purchase["date"])
            purchase["update_date"] = datetime.datetime.fromisoformat(
                purchase["update_date"]
            )
            assert purchase in purchases
        
        # post
        sell_add = await client.post("/sellers/new/", json=seller_to_add)
        purch_add = await client.post("/purchases/new/", json=purchase_to_add)
        
        seller_added = await client.get(f"/sellers/{seller_to_add['id']}/")
        purchase_added = await client.get(f"/purchases/{purchase_to_add['id']}/")
        
        assert sell_add.status_code == 200
        assert purch_add.status_code == 200
        
        # NOTE: 
        # Because in orm fields date and update_date set authomaticly - in `purchase_to_add` attrs 
        # `date` and `update_date` were deleted and set here. But `seller_to_add` don't changed, 
        # because it have date only, not datetime: date always work correctly, unlike datetime 
        # which have seconds and milliseconds in database.
        purchase_to_add["date"] = purchase_added.json()["date"]
        purchase_to_add["update_date"] = purchase_added.json()["update_date"]

        assert seller_added.json() == seller_to_add
        assert purchase_added.json() == purchase_to_add
        
        
        
        
