from fastapi import APIRouter
from pydantic import BaseModel

from Backend.agents.thumbnail_image_agent import (
    generate_thumbnail_image_prompt,
)

router = APIRouter()


class ThumbnailRequest(BaseModel):
    topic: str


@router.post("/thumbnail-image")
def thumbnail_image(req: ThumbnailRequest):

    prompt = generate_thumbnail_image_prompt(req.topic)

    return {
        "prompt": prompt
    }