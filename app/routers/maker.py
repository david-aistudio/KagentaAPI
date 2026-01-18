from fastapi import APIRouter, File, UploadFile, Form
from app.services.zenzxz import zenzxz_service
from typing import Optional

router = APIRouter(prefix="/maker", tags=["Maker"])

@router.get("/brat")
async def brat(text: str): return await zenzxz_service.brat(text)

@router.get("/brat-video")
async def brat_video(text: str): return await zenzxz_service.brat_video(text)

@router.get("/carbon")
async def carbon(input: str, title: Optional[str] = None): return await zenzxz_service.carbon(input, title)

@router.get("/fake-call")
async def fake_call(nama: str, durasi: str, avatar: str): return await zenzxz_service.fake_call(nama, durasi, avatar)

@router.get("/fake-iphone-chat")
async def fake_iphone_chat(text: str, chatime: str, statusbartime: str): return await zenzxz_service.fake_iphone_chat(text, chatime, statusbartime)

@router.get("/fake-fb")
async def fake_fb(name: str, comment: str, ppurl: str): return await zenzxz_service.fake_fb(name, comment, ppurl)

@router.get("/fake-story")
async def fake_story(username: str, caption: str, ppurl: str): return await zenzxz_service.fake_story(username, caption, ppurl)

@router.get("/meme")
async def meme(imageUrl: str, topText: Optional[str] = "", bottomText: Optional[str] = ""): return await zenzxz_service.meme_gen(imageUrl, topText, bottomText)

@router.get("/ttp")
async def ttp(text: str): return await zenzxz_service.ttp(text)

@router.get("/fake-tweet")
async def fake_tweet(username: str, name: str, tweet: str, profile: str, retweets: str, likes: str, quotes: str, client: str, theme: str = "light", image: Optional[str] = None):
    return await zenzxz_service.fake_tweet(username, name, tweet, profile, retweets, likes, quotes, client, theme, image)

@router.get("/ustadz-quote")
async def ustadz_quote(text: str): return await zenzxz_service.ustadz_quote(text)

@router.get("/yt-comment")
async def yt_comment(text: str, username: str, avatar: str): return await zenzxz_service.yt_comment(text, username, avatar)

@router.get("/magic-studio")
async def magic_studio(prompt: str): return await zenzxz_service.magic_studio(prompt)

# POST Endpoints (File Uploads)
@router.post("/fake-ml")
async def fake_ml(image: UploadFile = File(...), username: str = Form(...)):
    content = await image.read()
    return await zenzxz_service.fake_ml(content, username)

@router.post("/fake-story-v2")
async def fake_story_v2(profile_image: UploadFile = File(...), content_image: UploadFile = File(...), name: str = Form(...)):
    profile_content = await profile_image.read()
    content_content = await content_image.read()
    return await zenzxz_service.fake_story_v2(profile_content, content_content, name)

@router.post("/mpls-twibbon")
async def mpls_twibbon(file: UploadFile = File(...)):
    content = await file.read()
    return await zenzxz_service.mpls_twibbon(content)

@router.post("/jmk48-twibbon")
async def jmk48_twibbon(file: UploadFile = File(...)):
    content = await file.read()
    return await zenzxz_service.jmk48_twibbon(content)
