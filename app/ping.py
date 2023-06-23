from fastapi import APIRouter, Depends

from config import Settings, get_settings

router = APIRouter()

@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "vector_db": settings.vector_db,
        "vector_url": settings.vector_url,
        "llm_model_name": settings.llm_model_name,
        "template_name": settings.template_name,
    }