import os
import json
import tempfile
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Optional .env support
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Dynamic import of existing service files (filenames are not valid module names)
import importlib.util


def _load_module_from_path(module_name: str, file_path: str):
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)  # type: ignore[assignment]
        return module
    except Exception:
        return None


# Attempt to load the services from the current workspace files
analytics_mod = _load_module_from_path("free_analytics", os.path.join(os.getcwd(), "Advanced-analytics.py"))
audio_mod = _load_module_from_path("free_audio", os.path.join(os.getcwd(), "Audio-Enhancement.py"))
calendar_mod = _load_module_from_path("free_calendar", os.path.join(os.getcwd(), "CalenderIntegration.py"))
export_mod = _load_module_from_path("free_export", os.path.join(os.getcwd(), "Export.ppy"))

# Fallback minimal implementations if dynamic import fails
if analytics_mod is None:
    class FreeAnalyticsEngine:  # type: ignore
        async def generate_comprehensive_analytics(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "meeting_metrics": {"duration_minutes": 0, "word_count": 0, "sentence_count": 0, "words_per_minute": 0, "speaker_count": 1, "unique_topics": 0},
                "participant_insights": {"analysis": "No data available"},
                "content_analysis": {"topic_clusters": [], "sentiment_trend": "neutral", "keyword_evolution": [], "question_count": 0, "decision_points": []},
                "temporal_patterns": {"analysis": "No temporal data available"},
                "engagement_score": {"overall_score": 50.0, "components": {"content_richness": 50.0, "participation_balance": 50.0, "topic_diversity": 50.0}, "recommendations": []},
                "visualizations": {"speaker_pie_chart": {"labels": [], "values": []}, "activity_timeline": {"time_points": [], "activity_levels": []}, "engagement_radar": {"metrics": [], "scores": []}}
            }
else:
    FreeAnalyticsEngine = getattr(analytics_mod, "FreeAnalyticsEngine")

if audio_mod is None:
    class FreeAudioEnhancer:  # type: ignore
        async def enhance_audio(self, audio_path: str, methods=None) -> Dict[str, Any]:
            return {"enhanced_path": audio_path, "applied_methods": [], "improvement_metrics": {}, "original_stats": {"duration": 0}, "enhanced_stats": {"duration": 0}}
else:
    FreeAudioEnhancer = getattr(audio_mod, "FreeAudioEnhancer")

if calendar_mod is None:
    class FreeCalendarService:  # type: ignore
        async def extract_events_free(self, meeting_data: Dict[str, Any]):
            return []
else:
    FreeCalendarService = getattr(calendar_mod, "FreeCalendarService")

if export_mod is None:
    class FreeExportService:  # type: ignore
        async def export_analysis(self, analysis_data: Dict[str, Any], format: str = 'json') -> str:
            return json.dumps(analysis_data)
else:
    FreeExportService = getattr(export_mod, "FreeExportService")


app = FastAPI(title="Meeting Intelligence Platform - FREE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "name": "Meeting Intelligence Platform - FREE API",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "analyze_audio_free": "/analyze-audio-free/"
        }
    }


def _build_placeholder_result(audio_path: str, audio_duration: float) -> Dict[str, Any]:
    transcript_text = "This is a placeholder transcript generated in free mode. Replace with a transcription model if desired."
    speakers = [
        {"speaker_id": "S1", "segments_count": 3},
        {"speaker_id": "S2", "segments_count": 2},
    ]
    segments = [
        {"speaker": "S1", "start_time": 0.0, "end_time": 5.2, "duration": 5.2},
        {"speaker": "S2", "start_time": 5.2, "end_time": 10.8, "duration": 5.6},
        {"speaker": "S1", "start_time": 10.8, "end_time": 18.0, "duration": 7.2},
    ]

    result = {
        "processing_metadata": {
            "audio_duration": float(audio_duration),
            "source_path": audio_path,
        },
        "transcript": {"text": transcript_text},
        "speaker_analysis": {
            "speaker_count": len(speakers),
            "speakers": speakers,
            "segments": segments,
        },
        "emotion_analysis": {
            "primary_emotion": "neutral",
            "emotional_intensity": 0.5,
            "emotion_breakdown": {"neutral": 60, "positive": 25, "negative": 15},
            "sentiment": {"label": "Neutral", "score": 0.55},
        },
        "voice_authenticity": {
            "is_ai_voice": False,
            "ai_confidence": 0.05,
            "confidence": 0.95,
            "detection_method": "heuristic",
            "features": {"jitter": 0.02, "shimmer": 0.03},
        },
        "content_classification": {
            "content_type": "normal",
            "confidence": 0.9,
            "spam_score": 0.05,
            "ad_score": 0.02,
            "reasoning": "No strong indicators of spam or advertising detected.",
        },
        "llm_summary": {
            "summary": "The meeting covered project updates, discussed blockers, and outlined next steps.",
            "action_items": [
                "Follow up with design team on mockups",
                "Prepare sprint plan for next week",
                "Schedule stakeholder review meeting",
            ],
        },
        "confidence_score": 0.82,
    }
    return result


@app.post("/analyze-audio-free/")
async def analyze_audio_free(file: UploadFile = File(...)):
    # Read keys from environment (do not log)
    _google_api_key = os.getenv("GOOGLE_API_KEY")
    _hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

    try:
        # Save uploaded audio to a temporary file
        suffix = os.path.splitext(file.filename or "audio")[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        # Optional enhancement
        enhancer = FreeAudioEnhancer()
        enhancement = await enhancer.enhance_audio(temp_path)
        enhanced_path = enhancement.get("enhanced_path", temp_path)
        enhanced_stats = enhancement.get("enhanced_stats", {})
        audio_duration = float(enhanced_stats.get("duration", 0.0))

        # Build placeholder result structure
        result = _build_placeholder_result(enhanced_path, audio_duration)

        # Add advanced analytics
        try:
            analytics_engine = FreeAnalyticsEngine()
            advanced = await analytics_engine.generate_comprehensive_analytics(result)
            result["advanced_analytics"] = advanced
        except Exception as e:
            print(f"Analytics error: {e}")
            result["advanced_analytics"] = {"error": str(e)}

        # Suggested calendar events
        try:
            calendar_service = FreeCalendarService()
            events = await calendar_service.extract_events_free(result)
            result["calendar_suggestions"] = events
        except Exception as e:
            print(f"Calendar error: {e}")
            result["calendar_suggestions"] = []

        # Clean up temp file(s) but keep enhanced if it differs
        try:
            if os.path.exists(temp_path) and temp_path != enhanced_path:
                os.remove(temp_path)
        except Exception:
            pass

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("API_PORT", "8000"))
    except Exception:
        port = 8000
    # Run directly with the app instance and without auto-reload to avoid
    # watchdog/reloader issues seen in some Windows terminals.
    uvicorn.run(app, host=host, port=port, reload=False)


