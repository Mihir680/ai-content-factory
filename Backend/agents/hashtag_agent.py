from pathlib import Path
from Backend.services.gemini_service import generate_text


def generate_hashtags(topic):

    prompts = Path(
        "Backend/prompts/hashtags.txt"
    ).read_text(encoding="utf-8")

    prompts = prompts.format(topic=topic)

    return generate_text(prompts)