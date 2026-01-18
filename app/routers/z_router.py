from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.services.z_engine import z_engine

router = APIRouter(prefix="/z", tags=["Z-Engine"])

@router.get("/chat")
async def z_chat(message: str = Query(..., description="Message for GLM-4")):
    """
    Direct access to Z.ai (GLM-4) using your cookies.
    """
    return StreamingResponse(z_engine.chat_stream(message), media_type="text/event-stream")
