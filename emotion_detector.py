from transformers import pipeline

try:
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
except Exception as e:
    classifier = None
    print(f"Failed to load emotion model: {e}")

def detect_emotion(text: str) -> dict:
    if classifier is None:
        return {"emotion": "neutral", "intensity": 1.0}
    
    try:
        results = classifier(text)
        top_result = results[0][0]
        return {
            "emotion": top_result["label"],
            "intensity": float(top_result["score"])
        }
    except Exception as e:
        print(f"Error classifying text: {e}")
        return {"emotion": "neutral", "intensity": 1.0}
