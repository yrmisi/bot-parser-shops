__all__ = ("router",)
from aiogram import Router

from .hello import router as hello_router
from .search_object import router as search_object_router
from .until_the_new_year import router as until_the_new_year_router

router = Router(name=__name__)
router.include_routers(hello_router, search_object_router, until_the_new_year_router)
