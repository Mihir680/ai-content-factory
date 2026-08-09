import os
from pathlib import Path
from Backend.agents.script_agent import generate_script
from Backend.agents.title_agent import generate_titles
from Backend.agents.description_agent import generate_description
from Backend.agents.hashtag_agent import generate_hashtags
from Backend.agents.scene_agent import generate_scenes_and_images
from Backend.agents.video_agent import generate_video_from_scenes
from Backend.services.youtube_uploader import upload_video


def run_full_pipeline(
    topic: str,
    language: str = "English",
    platform: str = "YouTube",
    tone: str = "Professional",
    length: str = "1 Minute",
    visual_style: str = "real",
    auto_upload: bool = False,
    privacy_status: str = "private",
):
    """
    Full End-to-End Dynamic AI Video Pipeline:
    1. Generate Script (Gemini AI)
    2. Generate Title, Description, Hashtags
    3. Generate Content-Matched Multi-Scene AI Images (Flux AI)
    4. Render Clean MP4 Video + Generate Toggleable SRT Subtitle file
    5. (Optional) Auto-upload to YouTube with captions
    """
    print(f"Starting Content-Matched Pipeline for topic: '{topic}' (Style: {visual_style})")

    # Step 1: Script
    print("[Step 1] Generating AI Script...")
    script = generate_script(
        topic=topic,
        language=language,
        platform=platform,
        tone=tone,
        length=length,
    )

    # Step 2: Metadata / SEO
    print("[Step 2] Generating Title, Description & Hashtags...")
    titles = generate_titles(topic=topic, language=language, platform=platform, tone=tone)
    description = generate_description(topic=topic)
    hashtags = generate_hashtags(topic=topic)

    primary_title = titles.strip().split("\n")[0].replace("#", "").strip()
    if not primary_title:
        primary_title = topic

    # Step 3: Content-Matched AI Images
    print(f"[Step 3] Generating Content-Matched AI Scenes & Images ({visual_style} style)...")
    scenes = generate_scenes_and_images(script=script, topic=topic, platform=platform, visual_style=visual_style)


    # Step 4: Video Assembly + SRT Captions
    print("[Step 4] Rendering Clean MP4 Video & Generating SRT Subtitles...")
    render_result = generate_video_from_scenes(scenes, platform=platform)

    video_path = render_result["video_path"]
    srt_path = render_result["srt_path"]

    # Step 5: Optional Auto Upload
    upload_result = None
    if auto_upload:
        print("[Step 5] Auto-uploading to YouTube...")
        tag_list = [t.strip("#") for t in hashtags.split()] if hashtags else []
        upload_result = upload_video(
            video_path=video_path,
            title=primary_title,
            description=f"{description}\n\n{hashtags}",
            tags=tag_list,
            privacy_status=privacy_status,
        )

    print("Pipeline Completed Successfully!")
    return {
        "topic": topic,
        "title": primary_title,
        "script": script,
        "description": description,
        "hashtags": hashtags,
        "scenes_count": len(scenes),
        "video_path": video_path,
        "srt_path": srt_path,
        "upload_result": upload_result,
    }
