__all__ = ("router",)
from aiogram import Router

from .custom_routers import router as custom_routers_router
from .default_routers import router as default_routers_router

router = Router(name=__name__)
router.include_routers(custom_routers_router, default_routers_router)
