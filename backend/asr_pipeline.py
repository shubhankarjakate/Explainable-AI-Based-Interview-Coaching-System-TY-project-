from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3",
    device="cpu",          # force CPU
    compute_type="int8"    # optimized for CPU
)

segments, info = model.transcribe("audio.mp3")

for segment in segments:
    print(segment.text)