import httpx
from typing import Optional, List
from fastapi import UploadFile
from app.utils.spoof import get_headers

class ZenzxzService:
    BASE_URL = "https://api.zenzxz.my.id/api"

    async def _get(self, category: str, endpoint: str, params: dict = {}):
        headers = get_headers()
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.BASE_URL}/{category}/{endpoint}"
                response = await client.get(url, params=params, headers=headers, timeout=60)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e), "success": False}

    async def _post_multipart(self, category: str, endpoint: str, files: dict = {}, data: dict = {}):
        headers = get_headers()
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.BASE_URL}/{category}/{endpoint}"
                response = await client.post(url, data=data, files=files, headers=headers, timeout=60)
                response.raise_for_status()
                # Beberapa endpoint mungkin mengembalikan binary image langsung
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    return response.json()
                else:
                    return {"type": "binary", "content": response.content, "media_type": content_type}
            except httpx.HTTPError as e:
                return {"error": str(e), "success": False}

    # ================= AI =================
    async def copilot(self, message: str, model: str = "default"):
        return await self._get("ai", "copilotai", {"message": message, "model": model})

    async def felo(self, query: str):
        return await self._get("ai", "feloai", {"query": query})

    async def gemini(self, text: str, id: Optional[str] = None):
        params = {"text": text}
        if id: params["id"] = id
        return await self._get("ai", "gemini", params)

    async def gpt(self, question: str, prompt: str = "You are a helpful assistant"):
        return await self._get("ai", "gpt", {"question": question, "prompt": prompt})

    async def jeeves(self, prompt: str):
        return await self._get("ai", "jeevesai", {"prompt": prompt})

    async def writecream(self, question: str, logic: str = "general"):
        return await self._get("ai", "write-cream", {"question": question, "logic": logic})
    
    async def flux(self, prompt: str):
        return await self._get("ai", "flux", {"prompt": prompt})

    async def lyrics_generator(self, prompt: str):
        return await self._get("ai", "lyricsgenerator", {"prompt": prompt})

    async def story_generator(self, text: str, client: str = "web", mode: str = "creative", length: str = "Short"):
        return await self._get("ai", "storygenerator", {"text": text, "client": client, "mode": mode, "length": length})

    async def style_generator(self, prompt: str):
        return await self._get("ai", "stylegenerator", {"prompt": prompt})

    async def nano_banana(self, image: bytes, prompt: str):
        # POST Multipart
        return await self._post_multipart("ai", "nanobanana", files={"image": image}, data={"prompt": prompt})


    # ================= DOWNLOADER =================
    async def instagram_dl(self, url: str):
        return await self._get("downloader", "instagram", {"url": url})

    async def tiktok_dl(self, url: str):
        return await self._get("downloader", "douyin", {"url": url})

    async def spotify_dl(self, url: str):
        return await self._get("downloader", "spotify", {"url": url})

    async def soundcloud_dl(self, url: str):
        return await self._get("downloader", "soundcloud", {"url": url})

    async def webmusic_dl(self, url: str):
        return await self._get("downloader", "webmusic", {"url": url})

    async def npm_dl(self, query: str):
        return await self._get("downloader", "npm", {"query": query})

    async def twitter_dl(self, url: str):
        return await self._get("downloader", "twitter", {"url": url})

    async def ytmp3(self, url: str):
        return await self._get("downloader", "ytmp3", {"url": url})

    async def ytmp4(self, url: str, resolution: str = "720"):
        return await self._get("downloader", "ytmp4", {"url": url, "resolution": resolution})

    async def threads_dl(self, url: str):
        return await self._get("downloader", "threads", {"url": url})


    # ================= SEARCH =================
    async def applemusic_search(self, keyword: str):
        return await self._get("search", "applemusic", {"keyword": keyword})

    async def spotify_search(self, query: str):
        return await self._get("search", "spotify", {"query": query})

    async def google_image(self, query: str):
        return await self._get("search", "googleimage", {"query": query})

    async def gsmarena(self, query: str):
        return await self._get("search", "gsmarena", {"query": query})

    async def pinterest(self, query: str):
        return await self._get("search", "pinterest", {"query": query})

    async def play_youtube(self, query: str):
        return await self._get("search", "play", {"query": query})

    async def tiktok_search(self, query: str):
        return await self._get("search", "tiktok", {"query": query})

    async def wikipedia(self, query: str):
        return await self._get("search", "wikipedia", {"query": query})

    async def youtube_search(self, query: str):
        return await self._get("search", "youtube", {"query": query})


    # ================= MAKER =================
    async def brat(self, text: str):
        return await self._get("maker", "brat", {"text": text})

    async def brat_video(self, text: str):
        return await self._get("maker", "bratvid", {"text": text})

    async def carbon(self, input_code: str, title: Optional[str] = None):
        params = {"input": input_code}
        if title: params["title"] = title
        return await self._get("maker", "carbonify", params)

    async def fake_call(self, nama: str, durasi: str, avatar: str):
        return await self._get("maker", "fakecall", {"nama": nama, "durasi": durasi, "avatar": avatar})

    async def fake_iphone_chat(self, text: str, chatime: str, statusbartime: str):
        return await self._get("maker", "fakechatiphone", {"text": text, "chatime": chatime, "statusbartime": statusbartime})

    async def fake_fb(self, name: str, comment: str, ppurl: str):
        return await self._get("maker", "fakefb", {"name": name, "comment": comment, "ppurl": ppurl})

    async def fake_story(self, username: str, caption: str, ppurl: str):
        return await self._get("maker", "fakestory", {"username": username, "caption": caption, "ppurl": ppurl})

    async def meme_gen(self, image_url: str, top_text: Optional[str] = "", bottom_text: Optional[str] = ""):
        return await self._get("maker", "memegen", {"imageUrl": image_url, "topText": top_text, "bottomText": bottom_text})

    async def ttp(self, text: str):
        return await self._get("maker", "ttp", {"text": text})

    async def fake_tweet(self, username: str, name: str, tweet: str, profile: str, retweets: str, likes: str, quotes: str, client: str, theme: str = "light", image: Optional[str] = None):
        params = {
            "username": username, "name": name, "tweet": tweet, "profile": profile,
            "retweets": retweets, "likes": likes, "quotes": quotes, "client": client, "theme": theme
        }
        if image: params["image"] = image
        return await self._get("maker", "tweet", params)

    async def ustadz_quote(self, text: str):
        return await self._get("maker", "ustadz", {"text": text})

    async def yt_comment(self, text: str, username: str, avatar: str):
        return await self._get("maker", "ytcomment", {"text": text, "username": username, "avatar": avatar})

    async def magic_studio(self, prompt: str):
        return await self._get("maker", "magicstudio", {"prompt": prompt})

    # POST Makers (File Upload)
    async def fake_ml(self, image: bytes, username: str):
        return await self._post_multipart("maker", "fakeml", files={"image": image}, data={"username": username})

    async def fake_story_v2(self, profile_image: bytes, content_image: bytes, name: str):
        files = {"profile_image": profile_image, "content_image": content_image}
        return await self._post_multipart("maker", "fakestoryv2", files=files, data={"name": name})

    async def mpls_twibbon(self, file: bytes):
        return await self._post_multipart("maker", "mpls", files={"file": file})

    async def jmk48_twibbon(self, file: bytes):
        return await self._post_multipart("maker", "jomok48", files={"file": file})


    # ================= RANDOM =================
    async def random_blue_archive(self): return await self._get("random", "bluearchive")
    async def random_china(self): return await self._get("random", "china")
    async def random_indonesia(self): return await self._get("random", "indonesia")
    async def random_jepang(self): return await self._get("random", "jepang")

zenzxz_service = ZenzxzService()