from .products.routes import products_router
from .categories.routes import categories_router
from .purchases.routes import purchases_router
from .sellers.routes import sellers_router

__all__ = [
    "products_router",
    "categories_router",
    "purchases_router",
    "sellers_router",
]
