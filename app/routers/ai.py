from fastapi import APIRouter, File, UploadFile, Form
from app.services.zenzxz import zenzxz_service
from typing import Optional

router = APIRouter(prefix="/ai", tags=["AI Chat"])

@router.get("/copilot")
async def copilot(message: str, model: str = "default"): return await zenzxz_service.copilot(message, model)

@router.get("/felo")
async def felo(query: str): return await zenzxz_service.felo(query)

@router.get("/gemini")
async def gemini(text: str, id: Optional[str] = None): return await zenzxz_service.gemini(text, id)

@router.get("/gpt")
async def gpt(question: str, prompt: str = "You are a helpful assistant"): return await zenzxz_service.gpt(question, prompt)

@router.get("/jeeves")
async def jeeves(prompt: str): return await zenzxz_service.jeeves(prompt)

@router.get("/writecream")
async def writecream(question: str, logic: str = "general"): return await zenzxz_service.writecream(question, logic)

@router.get("/flux")
async def flux(prompt: str): return await zenzxz_service.flux(prompt)

@router.get("/lyrics")
async def lyrics(prompt: str): return await zenzxz_service.lyrics_generator(prompt)

@router.get("/story")
async def story(text: str, client: str = "web", mode: str = "creative", length: str = "Short"): 
    return await zenzxz_service.story_generator(text, client, mode, length)

@router.get("/music-style")
async def music_style(prompt: str): return await zenzxz_service.style_generator(prompt)

@router.post("/nano-banana")
async def nano_banana(image: UploadFile = File(...), prompt: str = Form(...)):
    content = await image.read()
    return await zenzxz_service.nano_banana(content, prompt)