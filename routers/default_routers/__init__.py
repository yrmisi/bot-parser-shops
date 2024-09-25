__all__ = ("router",)
from aiogram import Router

from .start import router as start_router
from .help import router as help_router
from .echo import router as echo_router

router = Router()
router.include_routers(start_router, help_router, echo_router)
