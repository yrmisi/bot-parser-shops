__all__ = ("router",)
from aiogram import Router

from .start_store_search import router as start_store_search_router
from .selection_of_categories import router as selection_of_categories_router
from .product_search import router as product_search_router
from .parsing_of_goods import router as parsing_of_goods_router


router = Router(name=__name__)
router.include_routers(
    start_store_search_router,
    selection_of_categories_router,
    product_search_router,
    parsing_of_goods_router,
)
