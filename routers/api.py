from fastapi import APIRouter

router = APIRouter()


@router.get("/permissions")
async def permissions():
    return ["V1", "V2"]
