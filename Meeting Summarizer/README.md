# Meeting Intelligence Platform (Free)

Local Streamlit UI + FastAPI backend for analyzing meeting audio with zero paid dependencies. Ships with free heuristics and clear upgrade paths to real models.

## Features and models
- Transcription: placeholder text (upgrade: Whisper/faster-whisper, WhisperX)
- Speaker diarization: placeholder segments (upgrade: pyannote.audio)
- Emotion/sentiment: heuristic label and score (upgrade: HF text emotion models; SER for audio)
- Voice authenticity: heuristic features (upgrade: ASVspoof/deepfake models, RawNet2 variants)
- Content classification: heuristic normal/spam/ads (upgrade: HF zero-shot `facebook/bart-large-mnli` or fine-tuned DistilBERT)
- AI summary + action items: template output (upgrade: Google Gemini, OpenAI GPT-4.x, local LLMs)
- Advanced analytics: stats/heuristics (topics, trends) via `FreeAnalyticsEngine`
- Audio enhancement: `librosa`, `noisereduce`, `scipy`, `soundfile` via `FreeAudioEnhancer`
- Calendar suggestions + ICS: rule-based via `FreeCalendarService`
- Export: JSON/CSV/TXT/HTML via `FreeExportService`

## Repo layout
```
app.py                      # Streamlit UI
server.py                   # FastAPI API (free-mode placeholder + analytics)
Advanced-analytics.py       # FreeAnalyticsEngine
Audio-Enhancement.py        # FreeAudioEnhancer
CalenderIntegration.py      # FreeCalendarService
Export.ppy                  # FreeExportService
requirements.txt            # Dependencies
```

## Quick start (Windows PowerShell)
1) Create venv and install deps
```powershell
cd "C:\Users\venkat\Desktop\New folder"
python -m venv .venv
.\.venv\Scripts\pip install -U pip
.\.venv\Scripts\pip install -r requirements.txt
```
2) (Optional) set keys
```powershell
$env:GOOGLE_API_KEY = "YOUR_GOOGLE_KEY"
$env:HUGGINGFACE_API_KEY = "YOUR_HF_KEY"
```
3) Run API
```powershell
.\.venv\Scripts\python server.py
# Health: http://127.0.0.1:8000/health
# Docs:   http://127.0.0.1:8000/docs
```
4) Run UI in another window
```powershell
.\.venv\Scripts\python -m streamlit run app.py
# UI: http://localhost:8501
```

## Using the UI
- Go to "Analyze Meeting", upload audio (wav/mp3/m4a/ogg/flac), click "Analyze Audio".
- Results appear in tabs: Summary, Transcript, Emotions, Speakers, Details, Export.

## Call the API directly
- Endpoint: POST `http://127.0.0.1:8000/analyze-audio-free/`
- Form field: `file` (audio binary)

Example:
```bash
curl -X POST -F "file=@sample.wav" http://127.0.0.1:8000/analyze-audio-free/
```

## Configuration
- `API_HOST` (default 127.0.0.1)
- `API_PORT` (default 8000)
- If you change port, update `self.api_url` in `app.py`.

## Upgrade paths (swap real models)
- Transcription: add faster-whisper in `server.py` before building the result
- Diarization: compute segments with pyannote and replace `speaker_analysis`
- Emotions: run HF classifier on transcript text
- Voice authenticity: compute spoof prob and set `voice_authenticity`
- Classification: zero-shot/fine-tuned classifier on transcript
- Summary: call Gemini/OpenAI/local LLM to fill `llm_summary`

## Troubleshooting
- UI error about Session State: launch with `python -m streamlit run app.py` (not `python app.py`)
- Connection refused in UI: ensure API is running and `http://127.0.0.1:8000/health` returns `{ "status":"ok" }`
- Don’t browse `0.0.0.0`; use `127.0.0.1` or `localhost`.

## License
Add your preferred license.
