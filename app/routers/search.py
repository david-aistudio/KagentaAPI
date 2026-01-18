from fastapi import APIRouter
from app.services.zenzxz import zenzxz_service

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/apple-music")
async def applemusic(keyword: str): return await zenzxz_service.applemusic_search(keyword)

@router.get("/spotify")
async def spotify(query: str): return await zenzxz_service.spotify_search(query)

@router.get("/google-image")
async def google_image(query: str): return await zenzxz_service.google_image(query)

@router.get("/gsmarena")
async def gsmarena(query: str): return await zenzxz_service.gsmarena(query)

@router.get("/pinterest")
async def pinterest(query: str): return await zenzxz_service.pinterest(query)

@router.get("/play-youtube")
async def play_youtube(query: str): return await zenzxz_service.play_youtube(query)

@router.get("/tiktok")
async def tiktok(query: str): return await zenzxz_service.tiktok_search(query)

@router.get("/wikipedia")
async def wikipedia(query: str): return await zenzxz_service.wikipedia(query)

@router.get("/youtube")
async def youtube(query: str): return await zenzxz_service.youtube_search(query)
