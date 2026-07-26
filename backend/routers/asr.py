from fastapi import APIRouter, UploadFile, File, HTTPException
from faster_whisper import WhisperModel
import tempfile
import shutil

router = APIRouter(prefix="/asr", tags=["asr"])


# Load model once at startup
try:
    model = WhisperModel(
        "large-v3",
        device="cpu",          # adjust to "cuda" if you have GPU
        compute_type="int8"    # optimized for CPU
    )
except Exception as e:
    # In case model fails to load, raise clear error on first use
    model = None
    load_error = str(e)
else:
    load_error = None


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Accept an audio file and return the transcribed text.
    Frontend can send webm/ogg/mp3 etc., Whisper handles most formats.
    """
    if load_error is not None or model is None:
        raise HTTPException(status_code=500, detail=f"ASR model failed to load: {load_error}")

    # Save upload to a temporary file because faster-whisper expects a path/bytes
    try:
        suffix = "." + (file.filename.split(".")[-1] if "." in file.filename else "webm")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        segments, _info = model.transcribe(tmp_path)
        text_parts = [segment.text.strip() for segment in segments if segment.text]
        full_text = " ".join(text_parts).strip()

        if not full_text:
            raise HTTPException(status_code=400, detail="No speech detected in audio.")

        return {"text": full_text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


