import httpx
import json
import random
from typing import Optional, AsyncGenerator

class NativeAIService:
    """
    Kagenta Native Engine (DuckDuckGo + Pollinations)
    100% Free, No Key, No Cookies Required.
    """
    
    DDG_STATUS_URL = "https://duckduckgo.com/duckchat/v1/status"
    DDG_CHAT_URL = "https://duckduckgo.com/duckchat/v1/chat"
    
    MODELS = {
        "gpt-4o": "gpt-4o-mini",
        "claude-3": "claude-3-haiku-20240307",
        "llama-3": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "mistral": "mistralai/Mistral-Small-24B-Instruct-2501",
        "o3-mini": "o3-mini"
    }

    async def _get_vqd(self) -> str:
        """Fetch the VQD token required for DuckDuckGo Chat"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-vqd-accept": "1"
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(self.DDG_STATUS_URL, headers=headers, timeout=10)
                resp.raise_for_status()
                return resp.headers.get("x-vqd-4")
            except Exception as e:
                print(f"[NativeAI] Error getting VQD: {e}")
                return None

    async def chat_stream(self, message: str, model_alias: str = "gpt-4o"):
        """
        Stream chat response from DuckDuckGo AI.
        Returns a generator yielding text chunks.
        """
        vqd = await self._get_vqd()
        if not vqd:
            yield "Error: Failed to initialize Native Engine (VQD missing)."
            return

        model_id = self.MODELS.get(model_alias, "gpt-4o-mini")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://duckduckgo.com/",
            "x-vqd-4": vqd,
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": message}]
        }

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
                                    yield data_json["message"]
                            except:
                                pass
            except Exception as e:
                yield f"Error during stream: {str(e)}"

    async def chat_complete(self, message: str, model_alias: str = "gpt-4o") -> dict:
        """
        Non-streaming chat. Waits for full response.
        """
        full_response = ""
        async for chunk in self.chat_stream(message, model_alias):
            full_response += chunk
        
        return {
            "status": True,
            "model": model_alias,
            "result": full_response,
            "engine": "Kagenta Native (DDG)"
        }

    # --- POLLINATIONS (Image) ---
    async def generate_image(self, prompt: str, model: str = "flux"):
        """
        Generate image using Pollinations.ai (No Key)
        """
        # Pollinations is a simple GET request that redirects to the image
        # We will return the URL directly or fetch the binary.
        safe_prompt = prompt.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?model={model}&nologo=true"
        
        return {
            "status": True,
            "image_url": url,
            "note": "Direct link. To download, use GET on this URL."
        }

native_service = NativeAIService()
