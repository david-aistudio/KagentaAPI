import httpx
import json
import asyncio
import uuid
import time
from typing import AsyncGenerator

class ZEngineService:
    """
    Kagenta Z-Engine v2 (Direct Reverse Engineering)
    Powered by GLM-4.7
    """
    
    BASE_URL = "https://chat.z.ai/api/v2/chat/completions"
    
    # Static headers from user's cURL
    HEADERS = {
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=0a0f6b8f17687240707416826e5990474fbb0b7de1a7d4c6b198a6f3a96224; _gcl_au=1.1.196834976.1768724073; _ga=GA1.1.726940261.1768724073; oauth_id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjdiZjU5NTQ4OWEwYmIxNThiMDg1ZTIzZTdiNTJiZjk4OTFlMDQ1MzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI4MDA0MjQzOTE5MjgtcXNxOTZ2YTN0cHVmcTRhamE4YTRhYmlvYm05MTBha3MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4MDA0MjQzOTE5MjgtcXNxOTZ2YTN0cHVmcTRhamE4YTRhYmlvYm05MTBha3MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTIyMDIwNjk4ODQyMTg0NzI3MTMiLCJlbWFpbCI6ImFkb2JldDU1MUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ik96OTlUVDBRWVdfYllxQ0otS09FS3ciLCJub25jZSI6IjI5SHFQa0JDQkhORHl3Uko0U2IwIiwibmFtZSI6IkFkb2JlIFRlc3QiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSnpaV1lERGYtQzdIS19KdXdoQ1RLRExYOWQ0TjFtVjZHcHY2MkJFdkd3YWVHR19RPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkFkb2JlIiwiZmFtaWx5X25hbWUiOiJUZXN0IiwiaWF0IjoxNzY4NzI0MTM2LCJleHAiOjE3Njg3Mjc3MzZ9.ZpO97cjz8HpQBdvmWfmFx_byi_SoXovO1Iek6NkOPmnSiozJom_NeJjgO0s8hIJ1ZpvNzrcj-DWTZUFwDOzhznWaypsgpi70xk6LUYaPYtnEOUupsdNVjO9TZYnTMTmU124El_VA0rI2hq-o6vbErmIBkGn93S3wjWI5iWHV2pHCNB-B4XcRuu2VBFBQDNSA2Zj4fU1EPlUS9Wdb-2znH9ym-ZUweQtJUwUjWEl6kapRK9ZDMg50VE0xUrB6t1Do91N26ehZIZTAhza8dQ8ie4IcOx4NVjw-DlBKwT3rbSFpOTYPCxSe7cGiitYPWDw5OwSYuublPWSycIZF2LpUjw; token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImVmNjljN2I0LWRhNzYtNDZiZi04ODQ5LWM3OWE3YmQxZDkyZSIsImVtYWlsIjoiYWRvYmV0NTUxQGdtYWlsLmNvbSJ9.mw0qroUEdldgIiILz3ETtVS2295o68ExUq3y_rf_bFOfbC43LEZA2eAoHjLxZ_L6nfn-1zOKuJI1d2COgTTWUQ; _ga_Z8QTHYBHP3=GS2.1.s1768724073$o1$g1$t1768725472$j18$l0$h0; ssxmod_itna=1-QqGx9DBDRGYWuix4qeqY5G7DRY3QR08D0dGMD3qq7t=GcD8rx0pxO356r3Gkb9aCDGKPMBPCnDdwDnnY4wKPnxNvDFhxhfFjiEfWzDBLdF6CLtYAP0OdGiMU1vTY/QxyFGH6ySfttWcDqS_4G4_tVQDixL_44BwhB932x9hD5iGtYdd2Dgk3dDCvG7CD3Nl_i5=YbjC5dCm4iFuDPew4qoiWk2p_x0m_kFuH3Iw01I1D2WG_cScxk1ivwzSEKcE5e/rAsb_avKoSAoiD; ssxmod_itna2=1-QqGx9DBDRGYWuix4qeqY5G7DRY3QR08D0dGMD3qq7t=GcD8rx0pxO356r3Gkb9aCDGKPMBPCnDdwDnnY4wKPnxNvDFhxhfFjiEfWzDBLdF6CLtYAP0OdGiMU1vTY/QxyFGH6ySfttWcDqS_4G4_tVQDixL_44BwhB932x9hD5iGtYdd2Dgk3dDCvG7CD3Nl_i5=YbjC5dCm4iFuDPew4qoiWk2p_x0m_kFuH3Iw01I1D2WG_cScxk1ivwzSEKcE5e/rAsb_avKoSAoiD', 
        'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImVmNjljN2I0LWRhNzYtNDZiZi04ODQ5LWM3OWE3YmQxZDkyZSIsImVtYWlsIjoiYWRvYmV0NTUxQGdtYWlsLmNvbSJ9.mw0qroUEdldgIiILz3ETtVS2295o68ExUq3y_rf_bFOfbC43LEZA2eAoHjLxZ_L6nfn-1zOKuJI1d2COgTTWUQ',
        'Origin': 'https://chat.z.ai',
        'Referer': 'https://chat.z.ai/c/87f955e9-c26d-4c96-9277-f9545070b3d0',
        'X-FE-Version': 'prod-fe-1.0.203',
        'X-Signature': 'feb256967a6500bd233fae5f5da219f3a7763c871fd95d9df3ee282eb769a53d',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
    }

    async def chat_stream(self, message: str):
        """
        Stream chat using Z.ai v2 Endpoint
        """
        ts = int(time.time() * 1000)
        req_id = str(uuid.uuid4())
        msg_id = str(uuid.uuid4())
        user_id = "ef69c7b4-da76-46bf-8849-c79a7bd1d92e"
        token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImVmNjljN2I0LWRhNzYtNDZiZi04ODQ5LWM3OWE3YmQxZDkyZSIsImVtYWlsIjoiYWRvYmV0NTUxQGdtYWlsLmNvbSJ9.mw0qroUEdldgIiILz3ETtVS2295o68ExUq3y_rf_bFOfbC43LEZA2eAoHjLxZ_L6nfn-1zOKuJI1d2COgTTWUQ"
        
        # Build query params
        params = {
            "timestamp": ts,
            "requestId": req_id,
            "user_id": user_id,
            "version": "0.0.1",
            "platform": "web",
            "token": token,
            "user_agent": self.HEADERS['User-Agent'],
            "language": "id-ID",
            "languages": "id-ID,id,en-US,en",
            "timezone": "Asia/Jakarta",
            "cookie_enabled": "true",
            "screen_width": "450",
            "screen_height": "1000",
            "host": "chat.z.ai",
            "hostname": "chat.z.ai",
            "protocol": "https:",
            "timezone_offset": "-420",
            "browser_name": "Chrome",
            "os_name": "Android",
            "signature_timestamp": ts
        }

        payload = {
            "stream": True,
            "model": "glm-4.7",
            "messages": [
                {"role": "user", "content": message}
            ],
            "signature_prompt": message[:10],
            "params": {},
            "extra": {},
            "features": {
                "image_generation": False,
                "web_search": False,
                "auto_web_search": False,
                "preview_mode": True,
                "flags": []
            },
            "chat_id": "87f955e9-c26d-4c96-9277-f9545070b3d0", # User's persistent chat
            "id": msg_id,
            "current_user_message_id": str(uuid.uuid4()),
            "current_user_message_parent_id": "0c7e1480-b363-4fd9-be82-ee67ad7971c5"
        }

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", self.BASE_URL, headers=self.HEADERS, params=params, json=payload, timeout=30) as response:
                    if response.status_code != 200:
                        yield f"Error: {response.status_code}\n"
                        error_body = await response.aread()
                        yield f"Response: {error_body.decode()}\n"
                        return

                    async for line in response.aiter_lines():
                        if line:
                            # Clean up SSE formatting for user
                            if line.startswith("data:"):
                                line = line.replace("data: ", "").strip()
                                try:
                                    data = json.loads(line)
                                    # Extract actual text from GLM stream
                                    if "choices" in data and len(data["choices"]) > 0:
                                        delta = data["choices"][0].get("delta", {})
                                        content = delta.get("content", "")
                                        if content:
                                            yield content
                                except:
                                    # If not JSON, yield raw line
                                    yield line + "\n"
                            else:
                                yield line + "\n"

            except Exception as e:
                yield f"[Z-Engine Error]: {str(e)}"

z_engine = ZEngineService()