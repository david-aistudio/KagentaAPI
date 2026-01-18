import httpx
import json
import asyncio
from typing import List, Dict, Any

class CombinedEngineService:
    """
    Kagenta Hybrid Engine v7.0
    - Chat: DuckDuckGo Native (GPT-4o Mini, Claude 3, Llama 3)
    - Image: Pollinations.ai (Flux, Turbo)
    """
    
    # --- DUCKDUCKGO CONFIG ---
    DDG_STATUS_URL = "https://duckduckgo.com/duckchat/v1/status"
    DDG_CHAT_URL = "https://duckduckgo.com/duckchat/v1/chat"
    
    DDG_MODELS = {
        "gpt-4o": "gpt-4o-mini",
        "claude-3": "claude-3-haiku-20240307",
        "llama-3": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "mistral": "mistralai/Mistral-Small-24B-Instruct-2501",
        "o3-mini": "o3-mini"
    }

    # --- POLLINATIONS IMAGE CONFIG ---
    IMAGE_URL = "https://image.pollinations.ai"
    IMAGE_MODELS = [
        "flux", "flux-pro", "flux-realism", "flux-anime", "flux-3d",
        "turbo", "stable-diffusion", "midijourney",
        "kontext", "nanobanana", "nanobanana-pro",
        "seedream", "seedream-pro", 
        "gptimage", "gptimage-large",
        "zimage", "veo", "seedance", "seedance-pro", "klein"
    ]

    async def _get_vqd(self) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-vqd-accept": "1"
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(self.DDG_STATUS_URL, headers=headers, timeout=10)
                if resp.status_code != 200:
                    print(f"[DDG Error] Status: {resp.status_code}, Body: {resp.text}")
                    return None
                return resp.headers.get("x-vqd-4")
            except Exception as e:
                print(f"[DDG Exception] {str(e)}")
                return None

    async def chat_complete(self, message: str, model: str = "gpt-4o") -> dict:
        """
        Non-streaming chat using DuckDuckGo.
        """
        vqd = await self._get_vqd()
        if not vqd:
            return {"status": False, "error": "Failed to initialize DDG Engine (VQD)"}

        model_id = self.DDG_MODELS.get(model, "gpt-4o-mini")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-vqd-4": vqd,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Referer": "https://duckduckgo.com/"
        }
        
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": message}]
        }

        full_text = ""
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", self.DDG_CHAT_URL, headers=headers, json=payload, timeout=30) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            data_str = line.replace("data: ", "").strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                data_json = json.loads(data_str)
                                if "message" in data_json:
                                    full_text += data_json["message"]
                            except:
                                pass
            except Exception as e:
                return {"status": False, "error": str(e)}

        return {
            "status": True,
            "model": model,
            "result": full_text,
            "engine": "Kagenta DDG Native"
        }

    async def generate_image(self, prompt: str, model: str = "flux", width: int = 1024, height: int = 1024):
        """Pollinations Image Gen"""
        safe_prompt = prompt.replace(" ", "%20")
        url = f"{self.IMAGE_URL}/prompt/{safe_prompt}?model={model}&width={width}&height={height}&nologo=true"
        return {"status": True, "image_url": url}

engine = CombinedEngineService()