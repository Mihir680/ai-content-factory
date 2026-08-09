import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from pathlib import Path
from moviepy import AudioArrayClip

print("🎵 Generating dynamic background music beat...")

audio_dir = Path("Backend/media/audio")
audio_dir.mkdir(parents=True, exist_ok=True)
bgm_path = audio_dir / "background.mp3"

sample_rate = 44100
duration = 120.0  # 120 seconds duration
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Smooth, relaxing lo-fi ambient pad synth score (Zero harsh kicks/clicks)
chord1 = 0.04 * np.sin(2 * np.pi * 220 * t) + 0.03 * np.sin(2 * np.pi * 277.18 * t) + 0.03 * np.sin(2 * np.pi * 329.63 * t)
chord2 = 0.04 * np.sin(2 * np.pi * 196 * t) + 0.03 * np.sin(2 * np.pi * 246.94 * t) + 0.03 * np.sin(2 * np.pi * 293.66 * t)
lfo = 0.5 * (1 + np.sin(2 * np.pi * 0.25 * t))  # Slow 4-second swell

audio_signal = (chord1 * lfo + chord2 * (1 - lfo)) * 0.4
audio_stereo = np.column_stack((audio_signal, audio_signal))

clip = AudioArrayClip(audio_stereo, fps=sample_rate)
clip.write_audiofile(str(bgm_path))


print("✅ Background music track generated:", bgm_path)
