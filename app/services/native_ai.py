import os
import sys

# --- MONKEY PATCH FOR VERCEL READ-ONLY FS ---
# This must run before g4f tries to load cookie directories
try:
    import platformdirs
    def mock_user_config_dir(appname=None, appauthor=None, version=None, roaming=True):
        return "/tmp"
    platformdirs.user_config_dir = mock_user_config_dir
except ImportError:
    pass

# Force home dir to /tmp just in case
os.environ["HOME"] = "/tmp"

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
        g4f.cookies.use_all_cookies = False

    async def chat_stream(self, message: str, model_alias: str = "gpt-4o"):
        """
        Stream chat response using g4f.
        """
        model_id = self.MODELS.get(model_alias, "gpt-4o")
        
        try:
            # Force Blackbox for stability on Vercel
            response = g4f.ChatCompletion.create(
                model=model_id,
                provider=g4f.Provider.Blackbox,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            for chunk in response:
                if chunk:
                    yield str(chunk)
                    await asyncio.sleep(0)

        except Exception as e:
            yield f"[Native Error]: {str(e)}"

    async def chat_complete(self, message: str, model_alias: str = "gpt-4o") -> dict:
        """
        Non-streaming chat.
        """
        model_id = self.MODELS.get(model_alias, "gpt-4o")
        try:
            # Explicitly use Blackbox or DuckDuckGo to avoid cookie scanning
            # Blackbox is usually the most robust free provider
            provider = g4f.Provider.Blackbox
            
            response = await g4f.ChatCompletion.create_async(
                model=model_id,
                provider=provider,
                messages=[{"role": "user", "content": message}]
            )
            return {
                "status": True,
                "model": model_alias,
                "result": response,
                "engine": "Kagenta Native (g4f:Blackbox)"
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
