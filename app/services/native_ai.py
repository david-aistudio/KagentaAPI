import os
import sys
import asyncio
import g4f

# --- LEVEL 10 MONKEY PATCHING (VERCEL GOD MODE) ---
# Memaksa seluruh operasi file G4F ke /tmp atau /dev/null
# Ini mencegah crash "Read-only file system"
try:
    # Patch platformdirs
    import platformdirs
    def mock_dirs(*args, **kwargs): return "/tmp"
    platformdirs.user_config_dir = mock_dirs
    platformdirs.user_cache_dir = mock_dirs
    platformdirs.user_data_dir = mock_dirs
    
    # Force Env Vars
    os.environ["G4F_COOKIES_DIR"] = "/tmp"
    os.environ["G4F_CACHE_DIR"] = "/tmp"
    os.environ["XDG_CACHE_HOME"] = "/tmp"
    os.environ["HOME"] = "/tmp"
except:
    pass

class NativeAIService:
    """
    Kagenta Native Engine v4.1 (Ultimate Edition)
    "The one that actually works."
    """
    
    # MAPPING MODEL -> PROVIDER YANG PASTI JALAN
    # Kita tidak pakai Auto, kita tembak provider yang terbukti "Gacor".
    MODEL_ROUTING = {
        "gpt-4o": g4f.Provider.Blackbox,   # Stabil, Cepat, Gratis
        "gpt-4": g4f.Provider.DuckDuckGo,  # Backup GPT-4
        "claude-3": g4f.Provider.Blackbox, # Blackbox punya Claude-3
        "llama-3": g4f.Provider.DeepInfra, # Sering open
        "gemini": g4f.Provider.Blackbox,   # Blackbox support Gemini
        "glm-4": g4f.Provider.GLM,         # Target utama GLM
        "mixtral": g4f.Provider.DeepInfra
    }

    def __init__(self):
        # Matikan semua logging sampah
        g4f.debug.logging = False
        g4f.debug.version_check = False
        # Matikan cookie loading (Vercel Killer)
        g4f.cookies.use_all_cookies = False

    async def chat_stream(self, message: str, model_alias: str = "gpt-4o"):
        """
        Stream chat dengan Failover System.
        """
        # 1. Tentukan Provider Utama
        provider = self.MODEL_ROUTING.get(model_alias, g4f.Provider.Blackbox)
        model_id = g4f.models.gpt_4o # Default generic model ID
        
        # Mapping nama model user ke ID internal G4F
        if model_alias == "glm-4":
            model_id = "glm-4" # Custom string often works for GLM provider
        elif "llama" in model_alias:
            model_id = g4f.models.llama_3_1_70b
        elif "claude" in model_alias:
            model_id = g4f.models.claude_3_5_sonnet
        
        try:
            # EKSEKUSI STREAM
            # Kita wrap dalam thread executor jika provider blocking, 
            # tapi G4F punya .create yang cukup pintar sekarang.
            
            response = g4f.ChatCompletion.create(
                model=model_id,
                provider=provider,
                messages=[{"role": "user", "content": message}],
                stream=True,
                ignore_stream=True # Force stream handling manually
            )
            
            for chunk in response:
                if chunk:
                    yield str(chunk)
                    await asyncio.sleep(0) # Yield control to event loop

        except Exception as e:
            # FAILOVER 1: DUCKDUCKGO (Backup Paling Aman)
            yield f"[Primary Failed: {str(e)}]. Switching to Backup...\n"
            try:
                backup_response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4o_mini,
                    provider=g4f.Provider.DuckDuckGo,
                    messages=[{"role": "user", "content": message}],
                    stream=True
                )
                for chunk in backup_response:
                    if chunk:
                        yield str(chunk)
                        await asyncio.sleep(0)
            except Exception as e2:
                yield f"[Critical Error]: Backup also failed. {str(e2)}"

    async def chat_complete(self, message: str, model_alias: str = "gpt-4o") -> dict:
        """
        Non-streaming chat wrapper.
        """
        full_text = ""
        async for chunk in self.chat_stream(message, model_alias):
            full_text += chunk
            
        return {
            "status": True,
            "model": model_alias,
            "result": full_text,
            "engine": "Kagenta Ultimate Native"
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