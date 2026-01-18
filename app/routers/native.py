from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.services.pollinations import pollinations

router = APIRouter(prefix="/native", tags=["Pollinations AI"])

@router.get("/models")
async def list_models(type: str = Query("chat", description="chat or image")):
    """Get list of available models"""
    return await pollinations.get_models(type)

@router.get("/chat")
async def chat(
    message: str = Query(..., description="Message"),
    model: str = Query("openai", description="Model ID (e.g. openai, claude, gemini, mistral)"),
    system: str = Query("You are a helpful assistant.", description="System Prompt")
):
    """
    Native Chat (Non-Streaming)
    """
    return await pollinations.chat_complete(message, model)

@router.get("/chat/stream")
async def chat_stream(
    message: str = Query(..., description="Message"),
    model: str = Query("openai", description="Model ID"),
    system: str = Query("You are a helpful assistant.", description="System Prompt")
):
    """
    Native Chat (Streaming)
    """
    return StreamingResponse(pollinations.chat_stream(message, model, system), media_type="text/event-stream")

@router.get("/image")
async def image(
    prompt: str = Query(..., description="Image Prompt"),
    model: str = Query("flux", description="Model ID (flux, turbo, etc)"),
    width: int = 1024,
    height: int = 1024
):
    """
    Native Image Generation
    """
    return await pollinations.generate_image(prompt, model, width, height)