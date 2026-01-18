import httpx
from fastapi import HTTPException

class NekolabsService:
    """
    Nekolabs Service - Premium Wrapper for TempMail & Tools
    """
    
    BASE_URL = "https://api.nekolabs.web.id"
    
    async def _get(self, endpoint: str):
        headers = {
            "User-Agent": "Kagenta-Premium-Client/1.0"
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{self.BASE_URL}{endpoint}", headers=headers, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as e:
                # Return graceful error for UI handling
                return {"status": False, "error": str(e), "message": "Upstream provider unavailable"}

    # --- TEMP MAIL V1 ---
    async def tempmail_v1_create(self):
        """Create random email (v1 engine)"""
        return await self._get("/tools/tempmail/v1/create")

    async def tempmail_v1_inbox(self, email: str):
        """Check inbox (v1 engine)"""
        # Nekolabs v1 usually requires just the email in query
        return await self._get(f"/tools/tempmail/v1/inbox?email={email}")

    # --- TEMP MAIL V2 (Faster/Cleaner) ---
    async def tempmail_v2_create(self):
        """Create random email (v2 engine)"""
        return await self._get("/tools/tempmail/v2/create")

    async def tempmail_v2_inbox(self, email: str):
        """Check inbox (v2 engine)"""
        return await self._get(f"/tools/tempmail/v2/inbox?email={email}")

nekolabs = NekolabsService()