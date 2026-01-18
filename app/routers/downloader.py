from fastapi import APIRouter
from app.services.zenzxz import zenzxz_service

router = APIRouter(prefix="/downloader", tags=["Downloader"])

@router.get("/instagram")
async def instagram(url: str): return await zenzxz_service.instagram_dl(url)

@router.get("/tiktok")
async def tiktok(url: str): return await zenzxz_service.tiktok_dl(url)

@router.get("/spotify")
async def spotify(url: str): return await zenzxz_service.spotify_dl(url)

@router.get("/soundcloud")
async def soundcloud(url: str): return await zenzxz_service.soundcloud_dl(url)

@router.get("/webmusic")
async def webmusic(url: str): return await zenzxz_service.webmusic_dl(url)

@router.get("/npm")
async def npm(query: str): return await zenzxz_service.npm_dl(query)

@router.get("/twitter")
async def twitter(url: str): return await zenzxz_service.twitter_dl(url)

@router.get("/ytmp3")
async def ytmp3(url: str): return await zenzxz_service.ytmp3(url)

@router.get("/ytmp4")
async def ytmp4(url: str, resolution: str = "720"): return await zenzxz_service.ytmp4(url, resolution)

@router.get("/threads")
async def threads(url: str): return await zenzxz_service.threads_dl(url)
