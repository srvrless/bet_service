from fastapi import APIRouter

from . import main

router = APIRouter()


router.include_router(
    main.router,
    prefix="/bets",
    tags=["bets"],
)
