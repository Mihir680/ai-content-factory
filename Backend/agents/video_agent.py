import os
import asyncio

import edge_tts
import numpy as np
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips

AUDIO_DIR = Path(__file__).resolve().parent.parent / "media" / "audio"
VIDEO_DIR = Path(__file__).resolve().parent.parent / "media" / "videos"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)


import re

async def generate_scene_voice(text: str, output_path: Path):
    """Generates natural, clear English/Gujarati/Hindi TTS voiceover audio for a scene."""
    voice = "en-US-ChristopherNeural"  # Default English Voice

    # Auto-detect language script
    if re.search(r"[\u0A80-\u0AFF]", text):
        voice = "gu-IN-NiranjanNeural"   # Gujarati Male Voice
    elif re.search(r"[\u0900-\u097F]", text):
        voice = "hi-IN-MadhurNeural"     # Hindi Male Voice

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+15%"  # Exciting, fast-paced viral Shorts voice!
    )

    await communicate.save(str(output_path))
    return str(output_path)



from PIL import ImageEnhance

def process_and_fit_image(image_path: str, output_path: str, target_size=(1920, 1080)):
    """Fits image to exact 16:9 aspect ratio and applies professional Hollywood color grading."""
    try:
        with Image.open(image_path) as img:
            img_rgb = img.convert("RGB")
            fitted = ImageOps.fit(img_rgb, target_size, method=Image.Resampling.LANCZOS)
            
            # Apply Color Correction & Grading
            contrast_enhancer = ImageEnhance.Contrast(fitted)
            graded = contrast_enhancer.enhance(1.15)  # Boost contrast
            
            color_enhancer = ImageEnhance.Color(graded)
            graded = color_enhancer.enhance(1.20)     # Boost vivid saturation
            
            sharpness_enhancer = ImageEnhance.Sharpness(graded)
            graded = sharpness_enhancer.enhance(1.25)  # Boost sharpness & clarity

            graded.save(output_path, "JPEG", quality=95)
            return output_path

    except Exception as e:
        print(f"[Image Process Error] {e}")
        return image_path



def add_subtitles_to_frame(pil_img, subtitle_text: str):
    """Overlays bold yellow/white viral subtitles onto the frame image."""
    if not subtitle_text:
        return pil_img

    img_copy = pil_img.copy()
    draw = ImageDraw.Draw(img_copy, "RGBA")
    w, h = img_copy.size

    # Wrap text into short readable lines
    words = subtitle_text.split()
    lines = []
    curr = ""
    for word in words:
        if len(curr + " " + word) > 36:
            lines.append(curr)
            curr = word
        else:
            curr = (curr + " " + word).strip()
    if curr:
        lines.append(curr)

    display_text = "\n".join(lines[:2])  # Max 2 lines per frame

    try:
        if re.search(r"[\u0A80-\u0AFF]", subtitle_text):
            font = ImageFont.truetype("C:/Windows/Fonts/shruti.ttf", 36)
        elif re.search(r"[\u0900-\u097F]", subtitle_text):
            font = ImageFont.truetype("C:/Windows/Fonts/Nirmala.ttc", 36)
        else:
            font = ImageFont.truetype("arialbd.ttf", 34)
    except Exception:
        font = ImageFont.load_default()


    bbox = draw.textbbox((0, 0), display_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (w - text_w) // 2
    y = h - text_h - 70

    # Draw dark translucent overlay banner
    pad_x, pad_y = 18, 12
    draw.rectangle(
        [x - pad_x, y - pad_y, x + text_w + pad_x, y + text_h + pad_y],
        fill=(0, 0, 0, 200)
    )

    # Draw vibrant yellow text with slight black shadow for max readability
    draw.text((x + 2, y + 2), display_text, fill=(0, 0, 0, 255), font=font, align="center")
    draw.text((x, y), display_text, fill=(255, 235, 20, 255), font=font, align="center")

    return img_copy


def generate_animated_moving_clip(image_path: str, duration: float, subtitle_text: str = "", motion_type: int = 0):
    """
    Renders 4 Hollywood dynamic camera motions:
    0: Zoom-In
    1: Pan-Right (Horizontal Sweep)
    2: Pan-Left (Horizontal Sweep)
    3: Tilt-Up (Vertical Reveal)
    """
    pil_img = Image.open(image_path).convert("RGB")
    w, h = pil_img.size

    def make_frame(t):
        progress = min(max(t / duration, 0.0), 1.0)
        scale = 1.18  # Extra border scale for panning room

        new_w, new_h = int(w * scale), int(h * scale)
        resized_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        max_dx = new_w - w
        max_dy = new_h - h

        if motion_type == 0:  # Dynamic Zoom In
            z_scale = 1.0 + 0.18 * progress
            zw, zh = int(w * z_scale), int(h * z_scale)
            z_img = pil_img.resize((zw, zh), Image.Resampling.LANCZOS)
            left = (zw - w) // 2
            top = (zh - h) // 2
            cropped = z_img.crop((left, top, left + w, top + h))
        elif motion_type == 1:  # Pan-Right
            left = int(max_dx * progress)
            top = max_dy // 2
            cropped = resized_img.crop((left, top, left + w, top + h))
        elif motion_type == 2:  # Pan-Left
            left = int(max_dx * (1.0 - progress))
            top = max_dy // 2
            cropped = resized_img.crop((left, top, left + w, top + h))
        else:  # Tilt-Up
            left = max_dx // 2
            top = int(max_dy * (1.0 - progress))
            cropped = resized_img.crop((left, top, left + w, top + h))

        # Add subtitle overlay
        frame_with_sub = add_subtitles_to_frame(cropped, subtitle_text)
        return np.array(frame_with_sub)

    from moviepy import VideoClip
    clip = VideoClip(make_frame, duration=duration)
    return clip



def generate_srt_subtitles(scenes: list, srt_path: Path):
    """Generates standard SubRip (.srt) subtitle file."""
    srt_content = []
    current_time = 0.0

    for idx, scene in enumerate(scenes, start=1):
        narration = scene.get("narration", "").strip()
        duration = scene.get("duration", 4.0)

        if not narration:
            continue

        start_str = format_srt_timestamp(current_time)
        end_str = format_srt_timestamp(current_time + duration)

        srt_block = f"{idx}\n{start_str} --> {end_str}\n{narration}\n"
        srt_content.append(srt_block)

        current_time += duration

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))

    print(f"[SRT] Created SRT Subtitle File: {srt_path}")
    return str(srt_path)


def format_srt_timestamp(seconds: float) -> str:
    """Formats float seconds into SRT timestamp HH:MM:SS,mmm"""
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def generate_video_from_scenes(scenes: list, platform: str = "YouTube"):
    """
    Renders multi-scene MP4 video with:
    1. Loud, crystal-clear voiceover audio
    2. Dynamic Ken Burns camera movement
    3. Dynamic Aspect Ratio (1080x1920 Vertical for Shorts/Reels vs 1920x1080 Widescreen for YouTube)
    4. Fast Ultrafast FFmpeg encoding
    """
    is_vertical = "short" in platform.lower() or "reel" in platform.lower() or "tiktok" in platform.lower()
    target_size = (1080, 1920) if is_vertical else (1920, 1080)

    clips = []
    audio_clips = []
    output_video_path = VIDEO_DIR / "video.mp4"
    output_srt_path = VIDEO_DIR / "video.srt"

    scene_data_for_srt = []

    for idx, scene in enumerate(scenes, start=1):
        narration = scene.get("narration", "").strip()
        image_path = scene.get("image_path")

        if not narration:
            continue

        # 1. Process image to exact platform target size (9:16 vertical vs 16:9 widescreen)
        clean_img_path = str(Path(image_path).parent / f"scene_{idx}_clean.jpg")
        process_and_fit_image(image_path, clean_img_path, target_size=target_size)


        # 2. Generate Audio Voiceover
        scene_audio_path = AUDIO_DIR / f"scene_{idx}.mp3"
        asyncio.run(generate_scene_voice(narration, scene_audio_path))

        # 3. Create Clean Video Clip with Ken Burns Motion Animation (No Subtitles)
        audio_clip = AudioFileClip(str(scene_audio_path))
        motion_choice = (idx - 1) % 4
        animated_clip = generate_animated_moving_clip(
            clean_img_path,
            duration=audio_clip.duration,
            subtitle_text="",  # Clean frame (No subtitles on video per user request)
            motion_type=motion_choice
        )

        animated_clip = animated_clip.with_audio(audio_clip)

        clips.append(animated_clip)
        audio_clips.append(audio_clip)

        scene_data_for_srt.append({
            "narration": narration,
            "duration": audio_clip.duration
        })

    if not clips:
        raise ValueError("No valid video scenes were generated.")

    # 4. Assembling animated video with combined audio stream
    print(f"[Video] Rendering {len(clips)} scenes with Voiceover & Motion...")
    final_video = concatenate_videoclips(clips, method="compose")

    if audio_clips:
        combined_voice = concatenate_audioclips(audio_clips)
        try:
            combined_voice.write_audiofile(str(AUDIO_DIR / "voice.mp3"), fps=44100)
        except Exception as e:
            print(f"[Audio Write Notice] {e}")

        bgm_path = AUDIO_DIR / "background.mp3"
        if bgm_path.exists():
            try:
                from moviepy import CompositeAudioClip
                bgm_clip = AudioFileClip(str(bgm_path)).with_duration(combined_voice.duration).with_volume_scaled(0.06)
                combined_audio = CompositeAudioClip([combined_voice, bgm_clip])
                print("[BGM] Mixed soft, smooth ambient background score underneath voiceover!")
            except Exception as e:
                print(f"[BGM Mix Notice] {e}")
                combined_audio = combined_voice

        else:
            combined_audio = combined_voice

        final_video = final_video.with_audio(combined_audio)



    import uuid
    temp_audio_path = str(AUDIO_DIR / f"temp_audio_{uuid.uuid4().hex[:8]}.m4a")

    final_video.write_videofile(
        str(output_video_path),
        fps=18,
        preset="ultrafast",
        threads=4,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-b:a", "192k", "-ar", "44100"],
        temp_audiofile=temp_audio_path,
        remove_temp=False
    )


    # Safe cleanup after handles released
    try:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
    except Exception:
        pass



    # 5. Generate SRT subtitles file
    srt_file_path = generate_srt_subtitles(scene_data_for_srt, output_srt_path)

    return {
        "video_path": str(output_video_path),
        "srt_path": srt_file_path
    }


def generate_video():
    """Compatibility alias for video router."""
    output_video_path = VIDEO_DIR / "video.mp4"
    return {"video_path": str(output_video_path)}