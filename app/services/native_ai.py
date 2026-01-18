import g4f
import asyncio
from typing import Optional, AsyncGenerator

class NativeAIService:
    """
    Kagenta Native Engine (Powered by g4f & Pollinations)
    The Ultimate Free AI Aggregator.
    """
    
    # Mapping friendly names to g4f model IDs
    MODELS = {
        "gpt-4o": "gpt-4o",
        "gpt-4": "gpt-4",
        "claude-3": "claude-3-haiku",
        "llama-3": "llama-3-70b",
        "mistral": "mistral-medium",
        "gemini": "gemini-pro"
    }

    def __init__(self):
        # Optimizations for Serverless/CLI
        g4f.debug.logging = False
        g4f.debug.version_check = False
        
        # FIX: Vercel is read-only, force cookie dir to /tmp
        import os
        os.environ["G4F_COOKIES_DIR"] = "/tmp"
        g4f.cookies.dir = "/tmp"
        g4f.cookies.use_all_cookies = False

    async def chat_stream(self, message: str, model_alias: str = "gpt-4o"):
        """
        Stream chat response using g4f (Auto-Provider).
        """
        model_id = self.MODELS.get(model_alias, "gpt-4o")
        
        try:
            # g4f's streaming is a generator, not async generator usually,
            # but we wrap it to be safe or use the sync iterator in a thread if needed.
            # For simplicity in FastAPI, we iterate the generator.
            
            response = g4f.ChatCompletion.create(
                model=model_id,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            for chunk in response:
                if chunk:
                    yield str(chunk)
                    # Small sleep to yield control in async loop if needed, 
                    # though g4f might block. In production, run in executor.
                    await asyncio.sleep(0)

        except Exception as e:
            yield f"[Native Error]: {str(e)}"

    async def chat_complete(self, message: str, model_alias: str = "gpt-4o") -> dict:
        """
        Non-streaming chat.
        """
        model_id = self.MODELS.get(model_alias, "gpt-4o")
        try:
            # Using create_async if available, else standard create
            response = await g4f.ChatCompletion.create_async(
                model=model_id,
                messages=[{"role": "user", "content": message}]
            )
            return {
                "status": True,
                "model": model_alias,
                "result": response,
                "engine": "Kagenta Native (g4f)"
            }
        except Exception as e:
            return {
                "status": False,
                "model": model_alias,
                "error": str(e),
                "engine": "Kagenta Native (g4f)"
            }

    # --- POLLINATIONS (Image) ---
    async def generate_image(self, prompt: str, model: str = "flux"):
        """
        Generate image using Pollinations.ai (No Key)
        """
        safe_prompt = prompt.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?model={model}&nologo=true"
        
        return {
            "status": True,
            "image_url": url,
            "note": "Direct link. To download, use GET on this URL."
        }

native_service = NativeAIService()
