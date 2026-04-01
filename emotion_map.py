def get_voice_params(emotion: str, intensity: float) -> dict:
    emotion_base = {
        "joy": {"speed": 1.2, "pitch": 4, "volume": 3},
        "sadness": {"speed": 0.8, "pitch": -3, "volume": -2},
        "anger": {"speed": 1.3, "pitch": 2, "volume": 6},
        "fear": {"speed": 1.1, "pitch": 1, "volume": -3},
        "surprise": {"speed": 1.25, "pitch": 5, "volume": 2},
        "disgust": {"speed": 0.9, "pitch": -2, "volume": 0},
        "neutral": {"speed": 1.0, "pitch": 0, "volume": 0}
    }
    
    base = emotion_base.get(emotion, emotion_base["neutral"])
    
    scaled_speed = 1.0 + (base["speed"] - 1.0) * intensity
    scaled_pitch = base["pitch"] * intensity
    scaled_volume = base["volume"] * intensity
    
    return {
        "speed": scaled_speed,
        "pitch": scaled_pitch,
        "volume": scaled_volume
    }
