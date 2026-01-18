from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.services.native_ai import native_service

router = APIRouter(prefix="/native", tags=["Native Engine"])

@router.get("/chat")
async def native_chat(
    message: str = Query(..., description="Your message"),
    model: str = Query("gpt-4o", description="Options: gpt-4o, claude-3, llama-3, mistral, o3-mini")
):
    """
    Kagenta Native Chat (Bypassed DDG API).
    Models: gpt-4o, claude-3, llama-3, mistral, o3-mini.
    """
    return await native_service.chat_complete(message, model)

@router.get("/chat/stream")
async def native_chat_stream(
    message: str = Query(..., description="Your message"),
    model: str = Query("gpt-4o", description="Options: gpt-4o, claude-3, llama-3, mistral, o3-mini")
):
    """
    Stream response (Server-Sent Events)
    """
    return StreamingResponse(native_service.chat_stream(message, model), media_type="text/event-stream")

@router.get("/image")
async def native_image(
    prompt: str = Query(..., description="Image Prompt"),
    model: str = Query("flux", description="Options: flux, turbo")
):
    """
    Kagenta Native Image (Pollinations).
    """
    return await native_service.generate_image(prompt, model)
