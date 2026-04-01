from gtts import gTTS
import pathlib

def generate_base_audio(text: str, output_path: str) -> str:
    out_path = pathlib.Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    tts = gTTS(text=text, lang="en")
    tts.save(str(out_path))
    return str(out_path)
