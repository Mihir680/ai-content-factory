from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from Backend.agents.script_agent import generate_script
from Backend.agents.seo_agent import generate_seo
from Backend.agents.description_agent import generate_description
from Backend.agents.hashtag_agent import generate_hashtags
from Backend.agents.thumbnail_agent import generate_thumbnail

router = APIRouter()


class GenerateRequest(BaseModel):
    topic: str


@router.post("/generate")
def generate(req: GenerateRequest):

    print("=" * 50)
    print("Generating Content For:", req.topic)
    print("=" * 50)

    try:
        script = generate_script(req.topic)
        print("✅ Script Generated")
    except Exception as e:
        print("❌ Script Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Script Error: {str(e)}")

    try:
        seo = generate_seo(req.topic)
        print("✅ SEO Generated")
    except Exception as e:
        print("❌ SEO Error:", str(e))
        raise HTTPException(status_code=500, detail=f"SEO Error: {str(e)}")

    try:
        description = generate_description(req.topic)
        print("✅ Description Generated")
    except Exception as e:
        print("❌ Description Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Description Error: {str(e)}")

    try:
        hashtags = generate_hashtags(req.topic)
        print("✅ Hashtags Generated")
    except Exception as e:
        print("❌ Hashtags Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Hashtags Error: {str(e)}")

    try:
        thumbnail = generate_thumbnail(req.topic)
        print("✅ Thumbnail Generated")
    except Exception as e:
        print("❌ Thumbnail Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Thumbnail Error: {str(e)}")

    print("🎉 All Content Generated Successfully")

    return {
        "script": script,
        "seo": seo,
        "description": description,
        "hashtags": hashtags,
        "thumbnail": thumbnail,
    }