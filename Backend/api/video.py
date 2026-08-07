from fastapi import APIRouter

from Backend.agents.video_agent import generate_video

router = APIRouter()


@router.post("/generate-video")
def generate():

    file = generate_video()

    return {
        "video": file
    }   