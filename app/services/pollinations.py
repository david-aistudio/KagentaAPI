import httpx
import json
import asyncio
from typing import AsyncGenerator, List, Dict, Any

class PollinationsService:
    """
    Kagenta Native Engine v6.0 (Pollinations.ai Official Wrapper)
    Zero-Auth, Unlimited, Multi-Model.
    """
    
    BASE_URL = "https://text.pollinations.ai"
    IMAGE_URL = "https://image.pollinations.ai"
    
    # --- MODEL DATABASE (AUTO-UPDATEABLE) ---
    MODELS_CHAT = [
        "openai", "openai-fast", "openai-large", "openai-reasoning", # GPT-4o, GPT-4o-mini, o1
        "claude", "claude-fast", "claude-large", # Claude 3.5 Sonnet, Haiku, Opus
        "gemini", "gemini-fast", "gemini-large", "gemini-search", # Gemini 1.5 Pro, Flash
        "mistral", "mistral-large", 
        "llama", "qwen-coder", "deepseek", 
        "grok", "minimax", "glm", "searchgpt"
    ]
    
    MODELS_IMAGE = [
        "flux", "flux-pro", "flux-realism", "flux-anime", "flux-3d",
        "turbo", "stable-diffusion"
    ]

    async def get_models(self, type: str = "chat") -> List[str]:
        """Fetch live models from Pollinations"""
        url = f"https://{'text' if type == 'chat' else 'image'}.pollinations.ai/models"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except:
                pass
        return self.MODELS_CHAT if type == "chat" else self.MODELS_IMAGE

    async def chat_stream(self, message: str, model: str = "openai", system_prompt: str = "You are a helpful assistant."):
        """
        Stream chat using OpenAI-Compatible Endpoint
        """
        url = f"{self.BASE_URL}/openai" # The Magic Endpoint
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "stream": True,
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json",
            # No Auth required for free tier, but we can add Referer to be polite
            "Referer": "https://pollinations.ai" 
        }

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", url, headers=headers, json=payload, timeout=60) as response:
                    if response.status_code != 200:
                        yield f"Error {response.status_code}: {await response.aread()}"
                        return

                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line.replace("data: ", "").strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                            except:
                                pass
            except Exception as e:
                yield f"[Error]: {str(e)}"

    async def chat_complete(self, message: str, model: str = "openai") -> dict:
        full_text = ""
        async for chunk in self.chat_stream(message, model):
            full_text += chunk
        return {"status": True, "model": model, "result": full_text}

    async def generate_image(self, prompt: str, model: str = "flux", width: int = 1024, height: int = 1024):
        safe_prompt = prompt.replace(" ", "%20")
        # Direct GET URL construction
        url = f"{self.IMAGE_URL}/prompt/{safe_prompt}?model={model}&width={width}&height={height}&nologo=true"
        return {"status": True, "image_url": url}

# Singleton
pollinations = PollinationsService()
