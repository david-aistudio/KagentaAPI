import os
import sys
import asyncio

# --- VERCEL COMPATIBILITY MODE ---
# Set env vars strictly for g4f internal use
os.environ["G4F_COOKIES_DIR"] = "/tmp"
os.environ["G4F_CACHE_DIR"] = "/tmp"
os.environ["XDG_CACHE_HOME"] = "/tmp"
# DO NOT set HOME to /tmp globally as it breaks other things

class NativeAIService:
    """
    Kagenta Native Engine v4.2 (Lazy Load Edition)
    Fixes Vercel 500 Crash by lazy loading g4f.
    """

    def __init__(self):
        pass

    async def chat_stream(self, message: str, model_alias: str = "gpt-4o"):
        """
        Stream chat with Lazy Loading.
        """
        try:
            # LAZY IMPORT G4F (Critical for Vercel)
            import g4f
            
            # Configure G4F at runtime
            g4f.debug.logging = False
            g4f.cookies.use_all_cookies = False
            
            # Routing Logic
            provider = g4f.Provider.Blackbox
            model_id = g4f.models.gpt_4o
            
            if model_alias == "glm-4":
                provider = g4f.Provider.GLM
                model_id = "glm-4"
            elif "llama" in model_alias:
                provider = g4f.Provider.DeepInfra
                model_id = g4f.models.llama_3_1_70b
            elif "claude" in model_alias:
                provider = g4f.Provider.Blackbox
                model_id = g4f.models.claude_3_5_sonnet

            response = g4f.ChatCompletion.create(
                model=model_id,
                provider=provider,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            for chunk in response:
                if chunk:
                    yield str(chunk)
                    await asyncio.sleep(0)

        except Exception as e:
            yield f"[Error: {str(e)}]. Try another model."

    async def chat_complete(self, message: str, model_alias: str = "gpt-4o") -> dict:
        full_text = ""
        async for chunk in self.chat_stream(message, model_alias):
            full_text += chunk
        return {
            "status": True,
            "model": model_alias,
            "result": full_text
        }

    # --- POLLINATIONS (Image) ---
    async def generate_image(self, prompt: str, model: str = "flux"):
        safe_prompt = prompt.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?model={model}&nologo=true"
        return {"status": True, "image_url": url}

native_service = NativeAIService()