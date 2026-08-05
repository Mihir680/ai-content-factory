from fastapi import APIRouter
from Backend.agents.research_agent import get_business_topics

router = APIRouter()

@router.get("/topics")
def topics():
    return {
        "topics": get_business_topics()
    }