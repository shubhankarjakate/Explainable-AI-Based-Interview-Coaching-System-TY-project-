from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import shutil
import os

from models.schemas import AudioEvaluationResult
from pipeline.audio_feature_extractor import extract_confidence_score


router = APIRouter(prefix="/audio", tags=["audio"])


@router.post("/evaluate", response_model=AudioEvaluationResult)
async def evaluate_audio(file: UploadFile = File(...)):
    """
    Accept an audio file and return a confidence score and related features.
    This wraps the existing audio_feature_extractor pipeline.
    """
    tmp_path = None
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No audio file provided.")

        suffix = "." + (file.filename.split(".")[-1] if "." in file.filename else "wav")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        result = extract_confidence_score(tmp_path)

        if not isinstance(result, dict) or "confidence_score" not in result:
            raise HTTPException(
                status_code=500,
                detail="Audio evaluation pipeline returned an invalid result."
            )

        return {
            "confidence_score": float(result.get("confidence_score", 0.0)),
            "level": str(result.get("level", "Unknown")),
            "transcript": str(result.get("transcript", "")),
            "features": result.get("features", {}),
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

