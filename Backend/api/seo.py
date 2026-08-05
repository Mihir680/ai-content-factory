from fastapi import APIRouter
from Backend.agents.seo_agent import generate_seo

router = APIRouter()

@router.get("/seo")
def seo(topic: str):
    return {
        "seo": generate_seo(topic)
    }