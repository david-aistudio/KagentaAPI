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

    async def chat_complete(self, message: str, model: str = "gpt-4o") -> dict:
        """
        Non-streaming chat using DuckDuckGo with session persistence.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
        }

        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            try:
                # 1. Get VQD (Phishing Method)
                landing_url = "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1"
                await client.get(landing_url, timeout=10)
                
                status_headers = {"x-vqd-accept": "1", "Referer": landing_url}
                status_resp = await client.get(self.DDG_STATUS_URL, headers=status_headers, timeout=10)
                
                vqd = status_resp.headers.get("x-vqd-4")
                if not vqd:
                    return {"status": False, "error": "Failed to extract VQD from session."}

                # 2. Send Chat
                model_id = self.DDG_MODELS.get(model, "gpt-4o-mini")
                chat_headers = {
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
                async with client.stream("POST", self.DDG_CHAT_URL, headers=chat_headers, json=payload, timeout=30) as response:
                    if response.status_code != 200:
                        return {"status": False, "error": f"DDG API Error: {response.status_code}"}
                        
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

                return {
                    "status": True,
                    "model": model,
                    "result": full_text or "Empty response.",
                    "engine": "Kagenta DDG Session-Native"
                }

            except Exception as e:
                return {"status": False, "error": f"Session Failure: {str(e)}"}

    async def generate_image(self, prompt: str, model: str = "flux", width: int = 1024, height: int = 1024):
        """Pollinations Image Gen"""
        safe_prompt = prompt.replace(" ", "%20")
        url = f"{self.IMAGE_URL}/prompt/{safe_prompt}?model={model}&width={width}&height={height}&nologo=true"
        return {"status": True, "image_url": url}

engine = CombinedEngineService()