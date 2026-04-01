from pydub import AudioSegment
import os
import pathlib

# Inject venv\Scripts into the PATH so pydub can find ffprobe.exe and ffmpeg.exe
scripts_dir = str(pathlib.Path(__file__).parent / "venv" / "Scripts")
if scripts_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = scripts_dir + os.pathsep + os.environ.get("PATH", "")

# Helps pydub find ffmpeg
AudioSegment.converter = "ffmpeg"

def modulate_voice(input_path: str, output_path: str, speed: float, pitch: float, volume: float) -> str:
    # Use pydub.AudioSegment; all paths via pathlib.Path
    in_path = pathlib.Path(input_path)
    out_path = pathlib.Path(output_path)
    
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")
        
    audio = AudioSegment.from_file(str(in_path))
    
    # Volume via sound + volume_db
    audio = audio + volume
    
    # Pitch via frame rate + resample trick
    # 1 octave = 12 semitones
    octaves = pitch / 12.0
    new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
    audio_pitch = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
    audio_resampled = audio_pitch.set_frame_rate(audio.frame_rate)
    
    # Speed via frame rate manipulation
    final_frame_rate = int(audio_resampled.frame_rate * speed)
    audio_final = audio_resampled._spawn(audio_resampled.raw_data, overrides={'frame_rate': final_frame_rate})
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    audio_final.export(str(out_path), format="mp3")
    
    return str(out_path)
