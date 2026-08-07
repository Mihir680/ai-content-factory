import edge_tts
import asyncio
from pathlib import Path

AUDIO_DIR = Path("Backend/media/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def generate_voice_async(text: str):
    output = AUDIO_DIR / "voice.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural"
    )

    await communicate.save(str(output))

    return str(output)


def generate_voice(text: str):
    return asyncio.run(generate_voice_async(text))