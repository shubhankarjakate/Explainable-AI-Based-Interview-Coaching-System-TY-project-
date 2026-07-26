"""
audio_feature_extractor.py
==========================
Full pipeline: audio file → confidence score.
Copy this file + confidence_score_model.pkl into your backend.

Install requirements:
    pip install pydub praat-parselmouth librosa openai-whisper joblib
    apt-get install ffmpeg   # or: brew install ffmpeg (macOS)

Usage:
    from audio_feature_extractor import extract_confidence_score

    result = extract_confidence_score("answer.wav")
    print(result["confidence_score"])  # e.g. 7.2
    print(result["transcript"])        # full speech text
    print(result["features"])          # all 9 acoustic features
"""

import os
import warnings
import numpy as np
warnings.filterwarnings("ignore")

FILLER_WORDS = [
    "um", "uh", "umm", "uhh", "hmm",
    "like", "basically", "actually", "literally",
    "you know", "i mean", "kind of", "sort of"
]

FEATURE_ORDER = [
    "pitch_mean", "pitch_var", "speech_rate", "pause_count",
    "avg_pause", "energy_mean", "jitter", "shimmer", "filler_words"
]


def extract_confidence_score(
    audio_path: str,
    model_path: str = "confidence_score_model.pkl",
    whisper_model_size: str = "base"
) -> dict:
    """
    Full pipeline: audio file -> confidence score.

    Args:
        audio_path        : path to audio file (any format)
        model_path        : path to confidence_score_model.pkl
        whisper_model_size: tiny (fast) | base (balanced) | small (accurate)

    Returns:
        dict:
            confidence_score : float (1.0-10.0)
            level            : str (Excellent/Good/Average/Below average/Poor)
            features         : dict of 9 acoustic features
            transcript       : str (full speech text - reuse for answer evaluation)
    """
    import joblib
    import librosa
    import parselmouth
    from parselmouth.praat import call
    import whisper as _whisper
    from pydub import AudioSegment

    # Step 1 - Convert to wav (16kHz mono)
    ext = os.path.splitext(audio_path)[1].lower().strip(".")
    wav_path = audio_path.replace(f".{ext}", "_tmp.wav") if ext else audio_path + "_tmp.wav"
    audio_seg = AudioSegment.from_file(audio_path, format=ext or "wav")
    audio_seg = audio_seg.set_channels(1).set_frame_rate(16000)
    audio_seg.export(wav_path, format="wav")

    try:
        # Step 2 - Pitch (parselmouth / Praat)
        sound = parselmouth.Sound(wav_path)
        pitch_obj = call(sound, "To Pitch", 0.0, 75, 600)
        pitch_vals = pitch_obj.selected_array["frequency"]
        voiced = pitch_vals[pitch_vals > 0]
        pitch_mean = float(np.mean(voiced)) if len(voiced) > 0 else 120.0
        pitch_var  = float(np.var(voiced))  if len(voiced) > 0 else 300.0

        # Step 3 - Jitter / shimmer (parselmouth / Praat)
        pp = call(sound, "To PointProcess (periodic, cc)", 75, 600)
        jitter  = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) * 100
        shimmer = call([sound, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6) * 100
        jitter  = float(jitter)  if not (np.isnan(jitter)  or np.isinf(jitter))  else 1.0
        shimmer = float(shimmer) if not (np.isnan(shimmer) or np.isinf(shimmer)) else 3.0

        # Step 4 - Energy (librosa RMS)
        y, sr = librosa.load(wav_path, sr=16000, mono=True)
        energy_mean = float(np.mean(librosa.feature.rms(y=y)[0]))

        # Step 5 - Pauses (librosa silence detection)
        intervals = librosa.effects.split(y, top_db=20, frame_length=2048, hop_length=512)
        pauses = []
        for i in range(1, len(intervals)):
            gap = (intervals[i][0] - intervals[i-1][1]) / sr
            if gap >= 0.2:
                pauses.append(gap)
        pause_count = len(pauses)
        avg_pause   = float(np.mean(pauses)) if pauses else 0.0

        # Step 6 - Speech rate + filler words (Whisper)
        wmodel = _whisper.load_model(whisper_model_size)
        result = wmodel.transcribe(
            wav_path, language="en", verbose=False,
            initial_prompt="Transcribe exactly as spoken including um, uh, like, you know, hmm."
        )
        transcript   = result["text"].strip()
        duration_sec = result["segments"][-1]["end"] if result["segments"] else len(y) / sr
        word_count   = len(transcript.split())
        speech_rate  = round(word_count / (duration_sec / 60.0), 3) if duration_sec > 0 else 0.0
        t_lower      = transcript.lower()
        filler_words = sum(t_lower.count(f) for f in FILLER_WORDS)

        features = {
            "pitch_mean"  : round(pitch_mean,  3),
            "pitch_var"   : round(pitch_var,   3),
            "speech_rate" : round(speech_rate, 3),
            "pause_count" : pause_count,
            "avg_pause"   : round(avg_pause,   3),
            "energy_mean" : round(energy_mean, 4),
            "jitter"      : round(jitter,      3),
            "shimmer"     : round(shimmer,     3),
            "filler_words": filler_words
        }

        # Step 7 - Predict confidence score
        try:
            mdl   = joblib.load(model_path)
            x     = np.array([[features[f] for f in FEATURE_ORDER]])
            score = round(float(np.clip(mdl.predict(x)[0], 1.0, 10.0)), 1)
            model_used = True
        except FileNotFoundError:
            # Fallback: simple rule-based score if model file is missing
            base = 7.0
            # Penalize many filler words
            base -= min(filler_words * 0.1, 3.0)
            # Penalize too many pauses
            base -= min(max(pause_count - 3, 0) * 0.2, 2.0)
            # Penalize very low energy
            if energy_mean < 0.01:
                base -= 1.0
            # Penalize extremely slow or extremely fast speech
            if speech_rate < 80:
                base -= 0.5
            if speech_rate > 180:
                base -= 0.5
            score = round(float(np.clip(base, 1.0, 10.0)), 1)
            model_used = False

        levels = [
            (8.0, "Excellent"),
            (6.0, "Good"),
            (4.0, "Average"),
            (2.0, "Below average"),
            (0.0, "Poor")
        ]
        level = next(l for threshold, l in levels if score >= threshold)

        return {
            "confidence_score": score,
            "level"           : level if model_used else f"{level} (heuristic)",
            "features"        : features,
            "transcript"      : transcript
        }

    finally:
        if os.path.exists(wav_path) and wav_path != audio_path:
            os.remove(wav_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python audio_feature_extractor.py <audio_file>")
        sys.exit(1)
    r = extract_confidence_score(sys.argv[1])
    print(f"Confidence Score : {r["confidence_score"]} / 10")
    print(f"Level            : {r["level"]}")
    print(f"Transcript       : {r["transcript"][:100]}")
    print("Features         :", r["features"])
