from fastapi import APIRouter
from app.services.zenzxz import zenzxz_service

router = APIRouter(prefix="/random", tags=["Random"])

@router.get("/blue-archive")
async def blue_archive(): return await zenzxz_service.random_blue_archive()

@router.get("/china")
async def china(): return await zenzxz_service.random_china()

@router.get("/indonesia")
async def indonesia(): return await zenzxz_service.random_indonesia()

@router.get("/jepang")
async def jepang(): return await zenzxz_service.random_jepang()
