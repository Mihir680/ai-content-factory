from pathlib import Path
from Backend.services.gemini_service import generate_text

BASE_DIR = Path(__file__).resolve().parent.parent


def generate_description(topic):
    prompts = (BASE_DIR / "prompts" / "description.txt").read_text(encoding="utf-8")
    prompts = prompts.format(topic=topic)
    return generate_text(prompts)