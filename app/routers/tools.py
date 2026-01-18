from fastapi import APIRouter, Query
from app.services.nekolabs import nekolabs

router = APIRouter(prefix="/tools", tags=["Premium Tools"])

@router.get("/tempmail/create")
async def create_email(version: str = Query("v2", description="Engine version (v1 or v2)")):
    """
    Generate a new premium temporary email address.
    """
    if version == "v1":
        return await nekolabs.tempmail_v1_create()
    return await nekolabs.tempmail_v2_create()

@router.get("/tempmail/inbox")
async def check_inbox(
    email: str = Query(..., description="Email address to check"),
    version: str = Query("v2", description="Engine version (v1 or v2)")
):
    """
    Fetch inbox messages live.
    """
    if version == "v1":
        return await nekolabs.tempmail_v1_inbox(email)
    return await nekolabs.tempmail_v2_inbox(email)
