from fastapi import APIRouter, HTTPException, Query
from app.services.zenzxz import zenzxz_service

router = APIRouter(prefix="/islamic", tags=["Islamic"])

@router.get("/adzan")
async def adzan(kota: str = Query(..., description="Nama kota, contoh: jakarta")):
    """Jadwal Adzan"""
    return await zenzxz_service.adzan(kota)

@router.get("/kisahnabi")
async def kisah_nabi(name: str = Query(..., description="Nama Nabi, contoh: adam")):
    """Kisah Nabi"""
    return await zenzxz_service.kisah_nabi(name)

@router.get("/jadwalsholat")
async def jadwal_sholat(kota: str = Query(..., description="Nama kota, contoh: bandung")):
    """Jadwal Sholat"""
    return await zenzxz_service.jadwal_sholat(kota)

@router.get("/quran")
async def quran(
    surah: str = Query(..., description="Nomor surah"),
    ayat: str = Query(..., description="Nomor ayat")
):
    """Ayat Al-Quran"""
    return await zenzxz_service.quran(surah, ayat)

@router.get("/hadits")
async def hadits(
    kitab: str = Query(..., description="Nama kitab hadits"),
    nomor: str = Query(..., description="Nomor hadits")
):
    """Cari Hadits"""
    return await zenzxz_service.hadits(kitab, nomor)
