from fastapi import APIRouter, Query
from app.services.hybrid_engine import engine

router = APIRouter(prefix="/native", tags=["Hybrid Engine"])

@router.get("/chat")
async def chat(
    message: str = Query(..., description="Message"),
    model: str = Query("gpt-4o", description="Options: gpt-4o, claude-3, llama-3, mistral, o3-mini")
):
    """
    Native Chat (DuckDuckGo Engine).
    No Stream. Pure JSON.
    """
    return await engine.chat_complete(message, model)

@router.get("/image")
async def image(
    prompt: str = Query(..., description="Image Prompt"),
    model: str = Query("flux", description="Options: flux, turbo, midijourney"),
    width: int = 1024,
    height: int = 1024
):
    """
    Native Image (Pollinations Engine).
    """
    return await engine.generate_image(prompt, model, width, height)
