from fastapi import APIRouter
from Backend.agents.script_agent import generate_script

router = APIRouter()

@router.get("/script")
def script(topic: str):
    return {
        "script": generate_script(topic)
    }