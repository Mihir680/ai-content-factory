from pathlib import Path
from Backend.services.gemini_service import generate_text

BASE_DIR = Path(__file__).resolve().parent.parent


def generate_scenes(topic):

    prompt = (
        BASE_DIR / "prompts" / "scenes.txt"
    ).read_text(encoding="utf-8")

    prompt = prompt.format(topic=topic)

    return generate_text(prompt)