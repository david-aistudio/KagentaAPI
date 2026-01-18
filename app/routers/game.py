from fastapi import APIRouter
from app.services.zenzxz import zenzxz_service

router = APIRouter(prefix="/game", tags=["Game"])

@router.get("/tebakgambar")
async def tebak_gambar():
    """Game Tebak Gambar"""
    return await zenzxz_service.tebak_gambar()

@router.get("/caklontong")
async def cak_lontong():
    """Game Cak Lontong"""
    return await zenzxz_service.cak_lontong()

@router.get("/tebaklagu")
async def tebak_lagu():
    """Game Tebak Lagu"""
    return await zenzxz_service.tebak_lagu()
