from fastapi import APIRouter
from app.services.zenzxz import zenzxz_service

router = APIRouter(prefix="/information", tags=["Information"])

@router.get("/gempa")
async def gempa():
    """Info Gempa Terkini"""
    return await zenzxz_service.gempa()

@router.get("/cuaca")
async def cuaca(kota: str):
    """Info Cuaca"""
    return await zenzxz_service.cuaca(kota)

@router.get("/liputan6")
async def liputan6():
    """Berita Liputan6"""
    return await zenzxz_service.liputan6()

@router.get("/kompas")
async def kompas():
    """Berita Kompas"""
    return await zenzxz_service.kompas()
