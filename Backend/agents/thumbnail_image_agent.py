from pathlib import Path
from Backend.services.gemini_service import generate_text


def generate_thumbnail_image_prompt(topic):

    prompt = Path(
        "Backend/prompts/thumbnail_image.txt"
    ).read_text(encoding="utf-8")

    prompt = prompt.format(topic=topic)

    return generate_text(prompt)