# The Empathy Engine

The Empathy Engine is a production-ready web application built for Windows 10/11 that detects the emotional tone of text and synthesizes speech modulated to express that emotion. The application uses a completely local stack for running inference and processing audio.

## Windows Setup Instructions

### Prerequisites
1. **Python**: Use Python 3.10+ from python.org. Ensure "Add Python to PATH" is checked during install.
2. **FFmpeg**: 
   - Download from https://ffmpeg.org/download.html -> extract zip -> add the `bin` folder to your System PATH manually.
   - Alternatively: `winget install ffmpeg` or `choco install ffmpeg` if Chocolatey is installed.

### Installation

1. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
   *(Note: DO NOT use `source venv/bin/activate` as Windows does not use that syntax)*
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

### Running the Server

Run the application using Uvicorn:
```cmd
uvicorn main:app --reload
```
Navigate to `http://127.0.0.1:8000` in your web browser.

## Architecture

```text
+-----------------------+      POST /synthesize       +-----------------------+
|                       |  ------------------------>  |                       |
|   Frontend (HTML/JS)  |                             |   FastAPI Backend     |
|                       |  <------------------------  |                       |
+-----------+-----------+      JSON + Audio URL       +---+---------+---------+
            |                                             |         |
            |                                             |         |
            |   +-----------------------------------------+         |
            |   |                                                   |
            v   v                                                   v
   +------------------+                              +-----------------------+
   |                  |                              |                       |
   | Emotion Detector |                              |       TTS Engine      |
   | (transformers)   |                              |         (gTTS)        |
   |                  |                              |                       |
   +------------------+                              +----------+------------+
                                                                |
                                                                |
                                                                v
                                                     +-----------------------+
                                                     |                       |
                                                     |    Voice Modulator    |
                                                     |       (pydub)         |
                                                     |                       |
                                                     +-----------------------+
```

## Emotion Mapping Table

The following table defines the audio parameter modifications per emotion relative to a neutral state (when intensity is 1.0).

| Emotion | Speed | Pitch | Volume |
|---------|-------|-------|--------|
| joy | 1.2 | +4 | +3 |
| sadness | 0.8 | -3 | -2 |
| anger | 1.3 | +2 | +6 |
| fear | 1.1 | +1 | -3 |
| surprise| 1.25| +5 | +2 |
| disgust | 0.9 | -2 | 0 |
| neutral | 1.0 | 0 | 0 |

