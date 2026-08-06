from pathlib import Path
from Backend.services.gemini_service import generate_text

BASE_DIR = Path(__file__).resolve().parent.parent


def generate_titles(
    topic,
    language="English",
    platform="YouTube",
    tone="Professional",
):

    prompt = (
        BASE_DIR / "prompts" / "title.txt"
    ).read_text(encoding="utf-8")

    prompt = prompt.format(
        topic=topic,
        language=language,
        platform=platform,
        tone=tone,
    )

    return generate_text(prompt)