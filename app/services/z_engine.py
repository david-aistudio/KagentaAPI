import httpx
import json
import asyncio
from typing import AsyncGenerator

class ZEngineService:
    """
    Kagenta Z-Engine (Powered by Zhipu AI / Z.ai Web Reverse Engineering)
    Uses user-provided cookies/tokens to bypass API limits.
    """
    
    BASE_URL = "https://chat.z.ai/api/v1"
    
    # Headers derived from user's cURL
    HEADERS = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=0a0f6b8f17687240707416826e5990474fbb0b7de1a7d4c6b198a6f3a96224; _gcl_au=1.1.196834976.1768724073; _ga=GA1.1.726940261.1768724073; oauth_id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjdiZjU5NTQ4OWEwYmIxNThiMDg1ZTIzZTdiNTJiZjk4OTFlMDQ1MzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI4MDA0MjQzOTE5MjgtcXNxOTZ2YTN0cHVmcTRhamE4YTRhYmlvYm05MTBha3MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4MDA0MjQzOTE5MjgtcXNxOTZ2YTN0cHVmcTRhamE4YTRhYmlvYm05MTBha3MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTIyMDIwNjk4ODQyMTg0NzI3MTMiLCJlbWFpbCI6ImFkb2JldDU1MUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ik96OTlUVDBRWVdfYllxQ0otS09FS3ciLCJub25jZSI6IjI5SHFQa0JDQkhORHl3Uko0U2IwIiwibmFtZSI6IkFkb2JlIFRlc3QiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSnpaV1lERGYtQzdIS19KdXdoQ1RLRExYOWQ0TjFtVjZHcHY2MkJFdkd3YWVHR19RPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkFkb2JlIiwiZmFtaWx5X25hbWUiOiJUZXN0IiwiaWF0IjoxNzY4NzI0MTM2LCJleHAiOjE3Njg3Mjc3MzZ9.ZpO97cjz8HpQBdvmWfmFx_byi_SoXovO1Iek6NkOPmnSiozJom_NeJjgO0s8hIJ1ZpvNzrcj-DWTZUFwDOzhznWaypsgpi70xk6LUYaPYtnEOUupsdNVjO9TZYnTMTmU124El_VA0rI2hq-o6vbErmIBkGn93S3wjWI5iWHV2pHCNB-B4XcRuu2VBFBQDNSA2Zj4fU1EPlUS9Wdb-2znH9ym-ZUweQtJUwUjWEl6kapRK9ZDMg50VE0xUrB6t1Do91N26ehZIZTAhza8dQ8ie4IcOx4NVjw-DlBKwT3rbSFpOTYPCxSe7cGiitYPWDw5OwSYuublPWSycIZF2LpUjw; token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImVmNjljN2I0LWRhNzYtNDZiZi04ODQ5LWM3OWE3YmQxZDkyZSIsImVtYWlsIjoiYWRvYmV0NTUxQGdtYWlsLmNvbSJ9.mw0qroUEdldgIiILz3ETtVS2295o68ExUq3y_rf_bFOfbC43LEZA2eAoHjLxZ_L6nfn-1zOKuJI1d2COgTTWUQ; _ga_Z8QTHYBHP3=GS2.1.s1768724073$o1$g1$t1768724986$j43$l0$h0; ssxmod_itna=1-QqGx9DBDRGYWuix4qeqY5G7DRY3QR08D0dGMD3qq7t=GcD8rx0pxO356r3Gkb9aDiqeqqK7OmPqSD0y6rDbTudDoxGArXDfG0YeqA70x0x=aju4pr4onmGMptC7A6h1dOuFYp9XHXeeiy1yYs=4DQZeDUxi1DG5DGYxDRxikD754Eh0YDeeDtx0rK4irN4D3Dec_bDDkDQKDXropD0RwCfhmvmYjv4DaDneDEl77e7dDNxDCM3Sww40WNFw44XeA04dDv2SoNta_U3uEf98ju3lYx6Wiw0PqUN7rkEDrll/Dwxn/Yjwte/NUDQ4gN3mI6AIYQ4j66UZ60owUAwZG5x2pxlqqiDgnXwQD5AwznXG7xe7xPChrBDdmeGlq5ADaftdYD; ssxmod_itna2=1-QqGx9DBDRGYWuix4qeqY5G7DRY3QR08D0dGMD3qq7t=GcD8rx0pxO356r3Gkb9aDiqeqqK7OmPqSD0y6rDbTudDoxGArXDfG0YeqA70x0x=aju4pr4onmGMptC7A6h1dOuFYp9XHXeeiy1yYs=4DQZeDUxi1DG5DGYxDRxikD754Eh0YDeeDtx0rK4irN4D3Dec_bDDkDQKDXropD0RwCfhmvmYjv4DaDneDEl77e7dDNxDCM3Sww40WNFw44XeA04dDv2SoNta_U3uEf98ju3lYx6Wiw0PqUN7rkEDrll/Dwxn/Yjwte/NUDQ4gN3mI6AIYQ4j66UZ60owUAwZG5x2pxlqqiDgnXwQD5AwznXG7xe7xPChrBDdmeGlq5ADaftdYD; ssxmod_itna2=1-QqGx9DBDRGYWuix4qeqY5G7DRY3QR08D0dGMD3qq7t=GcD8rx0pxO356r3Gkb9aDiqeqqK7OmPqwDnnAxD6GDATADFOvAfNw4eDsyf/RGx6zEDQj_18onar7RP1s6CH4pcbEMd3axzHt/lk6YIMo6KBLfUD2gtL2yAD0eXM=gUkRgzhiP9uh0Qf27bT6l9OXxlMuDr0NdeZ=Ke6XGGj3PRltt6TLOHWLtaB6H_AbPjAvZmp_xSL0H/WbnmwYidf354rgyRK9/CG0esgcYlaBKcPZkxIyCLSt5YDEkmyOqSk558p_dBPAIcRtG5xCG_Ki40I/3wPBau8aWDW4CDiQGxE0qrGUAe9WisKuLDRtzG_Ci5LR5OHe2B8U27SmZFgafYlADOQGDHW5cuyfgo2O=5xxmexNcPdYxKD4/ROjwmzg=83i9O=6w0W3P7iTr8_BvboGYF3qVSdq_1YRbNPxD2baROWiihMDCGtSx4/xWiGPSBrmHZmvbYGDD',
        'Referer': 'https://chat.z.ai/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImVmNjljN2I0LWRhNzYtNDZiZi04ODQ5LWM3OWE3YmQxZDkyZSIsImVtYWlsIjoiYWRvYmV0NTUxQGdtYWlsLmNvbSJ9.mw0qroUEdldgIiILz3ETtVS2295o68ExUq3y_rf_bFOfbC43LEZA2eAoHjLxZ_L6nfn-1zOKuJI1d2COgTTWUQ',
        'Origin': 'https://chat.z.ai'
    }

    async def chat_stream(self, message: str):
        """
        Stream chat using Z.ai web endpoint (Reverse Engineered)
        """
        # Create a new conversation first (or use existing if persistent)
        # Assuming we need to POST to /chats to create/continue
        # Based on typical GLM web API, we send message directly to a stream endpoint or chat endpoint.
        
        # NOTE: Guessing endpoint based on common structure, might need adjustment after first test
        # Standard web endpoint for Z.ai usually involves /api/v1/chats or /api/v1/stream
        # Let's try creating a completion.
        
        payload = {
            "model": "GLM-4", # Or specific ID if known
            "messages": [
                {"role": "user", "content": message}
            ],
            "stream": True,
            "temperature": 0.5,
            "top_p": 0.9
        }
        
        # Trying typical endpoint
        url = f"{self.BASE_URL}/chat/completions" # Common alias
        
        # Fallback if that's 404: Try the endpoint user found history at, but POST
        # url = f"{self.BASE_URL}/chats" 

        async with httpx.AsyncClient() as client:
            try:
                # First, try to guess the correct "send message" endpoint
                # Usually web apps POST to /chats or /chats/{id}/messages
                
                # Let's try to just hit the chat endpoint
                # Since we don't know the exact endpoint for NEW chat, let's try a standard one
                # If this fails, we will need to INSPECT the 'send' request from user, not just history list.
                # But let's try /api/v1/chats/stream or similar.
                
                # REVISION: Most Zhipu web proxies use this:
                url = "https://chat.z.ai/api/v1/stream" 
                
                async with client.stream("POST", url, headers=self.HEADERS, json=payload, timeout=30) as response:
                    if response.status_code != 200:
                         # If 404, try alternate
                         yield f"Status: {response.status_code}. Endpoint guessing failed."
                         return

                    async for line in response.aiter_lines():
                        if line:
                            # Parse SSE
                            if line.startswith("data:"):
                                yield line.replace("data: ", "") + "\n"
                            else:
                                yield line + "\n"

            except Exception as e:
                yield f"[Z-Engine Error]: {str(e)}"

z_engine = ZEngineService()
