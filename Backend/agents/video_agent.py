from moviepy import ImageClip, AudioFileClip
from pathlib import Path


def generate_video():

    image_path = Path("Backend/media/images/cover.jpg")
    audio_path = Path("Backend/media/audio/voice.mp3")
    output_path = Path("Backend/media/videos/video.mp4")

    audio = AudioFileClip(str(audio_path))

    video = (
        ImageClip(str(image_path))
        .with_duration(audio.duration)
        .with_audio(audio)
    )

    video.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )

    return str(output_path)