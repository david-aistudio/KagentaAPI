import httpx
import json
import asyncio
from typing import AsyncGenerator

class NativeAIService:
    """
    Kagenta Native Engine v5.0 (Manual Scraper Edition)
    Stable, Fast, No dependencies on g4f.
    """
    
    DDG_STATUS_URL = "https://duckduckgo.com/duckchat/v1/status"
    DDG_CHAT_URL = "https://duckduckgo.com/duckchat/v1/chat"
    
    # Supported Models in DDG
    MODELS = {
        "gpt-4o": "gpt-4o-mini",
        "claude-3": "claude-3-haiku-20240307",
        "llama-3": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "mistral": "mistralai/Mistral-Small-24B-Instruct-2501"
    }

    async def _get_vqd(self) -> str:
        """Fetch VQD token from DuckDuckGo"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-vqd-accept": "1"
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(self.DDG_STATUS_URL, headers=headers, timeout=10)
                return resp.headers.get("x-vqd-4")
            except:
                return None

    async def chat_stream(self, message: str, model_alias: str = "gpt-4o"):
        """
        Manual Stream Implementation for DuckDuckGo AI.
        """
        vqd = await self._get_vqd()
        if not vqd:
            yield "Error: Service unavailable (VQD Failure)."
            return

        model_id = self.MODELS.get(model_alias, "gpt-4o-mini")
        
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

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", self.DDG_CHAT_URL, headers=headers, json=payload, timeout=30) as response:
                    if response.status_code != 200:
                        yield f"Error {response.status_code}: {await response.aread()}\n"
                        return

                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            data_str = line.replace("data: ", "").strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                data_json = json.loads(data_str)
                                if "message" in data_json:
                                    yield data_json["message"]
                            except:
                                pass
            except Exception as e:
                yield f"[Error]: {str(e)}"

    async def chat_complete(self, message: str, model_alias: str = "gpt-4o") -> dict:
        """Non-streaming response wrapper"""
        full_text = ""
        async for chunk in self.chat_stream(message, model_alias):
            full_text += chunk
        
        return {
            "status": True,
            "model": model_alias,
            "result": full_text or "No response from AI.",
            "engine": "Kagenta Manual Native"
        }

    # --- POLLINATIONS (Image) ---
    async def generate_image(self, prompt: str, model: str = "flux"):
        safe_prompt = prompt.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?model={model}&nologo=true"
        return {
            "status": True,
            "image_url": url
        }

native_service = NativeAIService()
