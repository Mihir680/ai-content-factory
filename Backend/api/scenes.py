from fastapi import APIRouter
from pydantic import BaseModel

from Backend.agents.scene_agent import generate_scenes

router = APIRouter()


class SceneRequest(BaseModel):
    topic: str


@router.post("/generate-scenes")
def generate_scene(req: SceneRequest):
    return {
        "scenes": generate_scenes(req.topic)
    }