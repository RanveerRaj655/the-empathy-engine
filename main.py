from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import pathlib
from emotion_detector import detect_emotion
from emotion_map import get_voice_params
from tts_engine import generate_base_audio
from voice_modulator import modulate_voice
import uuid

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent

# Mount static files
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = BASE_DIR / "templates" / "index.html"
    try:
        content = index_path.read_text(encoding="utf-8")
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Index template not found.</h1>", status_code=404)

@app.post("/synthesize")
async def synthesize(text: str = Form(...)):
    # 1. Detect emotion
    emotion_data = detect_emotion(text)
    emotion = emotion_data["emotion"]
    intensity = emotion_data["intensity"]
    
    # 2. Get voice params
    params = get_voice_params(emotion, intensity)
    
    # 3. Generate voice file path
    unique_id = str(uuid.uuid4())
    temp_audio_path = static_dir / f"temp_{unique_id}.mp3"
    final_audio_path = static_dir / f"output_{unique_id}.mp3"
    
    # Generate base TTS
    generate_base_audio(text, str(temp_audio_path))
    
    # Modulate voice
    modulate_voice(
        input_path=str(temp_audio_path),
        output_path=str(final_audio_path),
        speed=params["speed"],
        pitch=params["pitch"],
        volume=params["volume"]
    )
    
    # Clean up temp base audio (optional)
    if temp_audio_path.exists():
        temp_audio_path.unlink()
        
    return JSONResponse(content={
        "emotion": emotion,
        "intensity": intensity,
        "audio_url": f"/static/{final_audio_path.name}",
        "params": params
    })
