from fastapi import APIRouter, Query
from app.services.nekolabs import nekolabs

router = APIRouter(prefix="/ai", tags=["Kagenta RAG"])

SYSTEM_PROMPT = """
[SYSTEM: You are KagentaBot, the AI Concierge for KagentaMail.]
[CONTEXT: KagentaMail is a premium, onyx-styled disposable email service.]
[RULES: Be elegant, concise, and helpful. Emails expire in 1 hour. Engine: Nekolabs v2.]
[USER QUESTION BELOW]
"""

@router.get("/chat")
async def chat(
    message: str = Query(..., description="User message"),
    model: str = Query("gpt5", description="copilot, gpt5, or perplexity"),
    context: str = Query("", description="Current email context")
):
    """
    RAG-enhanced Chat endpoint.
    """
    # RAG Injection
    full_prompt = f"{SYSTEM_PROMPT}\n[CURRENT EMAIL: {context}]\nUser: {message}"
    
    if model == "copilot":
        return await nekolabs.chat_copilot(full_prompt)
    elif model == "perplexity":
        return await nekolabs.chat_perplexity(full_prompt)
    else:
        return await nekolabs.chat_gpt5(full_prompt)
