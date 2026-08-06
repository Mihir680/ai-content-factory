from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from Backend.agents.title_agent import generate_titles
from Backend.agents.script_agent import generate_script
from Backend.agents.seo_agent import generate_seo
from Backend.database.database import SessionLocal
from Backend.database.crud import save_content
from Backend.agents.description_agent import generate_description
from Backend.agents.hashtag_agent import generate_hashtags
from Backend.agents.thumbnail_agent import generate_thumbnail

router = APIRouter()


class GenerateRequest(BaseModel):
    topic: str
    language: str = "English"
    platform: str = "YouTube"
    tone: str = "Professional"
    length: str = "5 Minutes"


@router.post("/generate")
def generate(req: GenerateRequest):

    print("=" * 50)
    print("Generating Content For:", req.topic)
    print("Language:", req.language)
    print("Platform:", req.platform)
    print("Tone:", req.tone)
    print("Length:", req.length)
    print("=" * 50)

    # Script
    try:
        script = generate_script(
            topic=req.topic,
            language=req.language,
            platform=req.platform,
            tone=req.tone,
            length=req.length,
        )
        print("✅ Script Generated")
    except Exception as e:
        print("❌ Script Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Script Error: {str(e)}",
        )

    # SEO
    try:
        seo = generate_seo(req.topic)
        print("✅ SEO Generated")
    except Exception as e:
        print("❌ SEO Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"SEO Error: {str(e)}",
        )

    # Description
    try:
        description = generate_description(req.topic)
        print("✅ Description Generated")
    except Exception as e:
        print("❌ Description Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Description Error: {str(e)}",
        )

    # Hashtags
    try:
        hashtags = generate_hashtags(req.topic)
        print("✅ Hashtags Generated")
    except Exception as e:
        print("❌ Hashtags Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Hashtags Error: {str(e)}",
        )

    # Thumbnail
    try:
        thumbnail = generate_thumbnail(req.topic)
        print("✅ Thumbnail Generated")
    except Exception as e:
        print("❌ Thumbnail Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Thumbnail Error: {str(e)}",
        )

    # Viral Titles
    try:
        titles = generate_titles(
            topic=req.topic,
            language=req.language,
            platform=req.platform,
            tone=req.tone,
        )
        print("✅ Titles Generated")
    except Exception as e:
        print("❌ Titles Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Titles Error: {str(e)}",
        )

    print("🎉 All Content Generated Successfully")

    db = SessionLocal()

    try:
        save_content(
            db=db,
            topic=req.topic,
            language=req.language,
            platform=req.platform,
            tone=req.tone,
            length=req.length,
            script=script,
            seo=seo,
            description=description,
            hashtags=hashtags,
            thumbnail=thumbnail,
            titles=titles,
        )
        print("✅ Saved To Database")
    finally:
        db.close()

    return {
        "script": script,
        "seo": seo,
        "description": description,
        "hashtags": hashtags,
        "thumbnail": thumbnail,
        "titles": titles,
    }