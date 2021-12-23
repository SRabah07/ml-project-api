from fastapi import APIRouter

router = APIRouter()


@router.get("/permissions")
async def home():
    return ["V1", "V2"]
