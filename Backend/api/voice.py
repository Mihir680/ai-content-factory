from fastapi import APIRouter
from pydantic import BaseModel

from Backend.agents.voice_agent import generate_voice

router = APIRouter()


class VoiceRequest(BaseModel):
    text: str


@router.post("/generate-voice")
def voice(req: VoiceRequest):

    file = generate_voice(req.text)

    return {
        "audio": file
    }