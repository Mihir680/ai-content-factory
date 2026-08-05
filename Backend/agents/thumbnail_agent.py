from pathlib import Path
from Backend.services.gemini_service import generate_text


def generate_thumbnail(topic):

    prompts = Path(
        "Backend/prompts/thumbnail.txt"
    ).read_text(encoding="utf-8")

    prompts = prompts.format(topic=topic)

    return generate_text(prompts)