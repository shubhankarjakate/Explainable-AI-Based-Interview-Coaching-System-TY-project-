from audio_feature_extractor import extract_confidence_score


def evaluate_answer(audio_file):

    result = extract_confidence_score(audio_file)

    return {
        "confidence_score": result["confidence_score"],
        "level": result["level"],
        "transcript": result["transcript"],
        "features": result["features"]
    }


if __name__ == "__main__":

    audio_file = "speech.wav"   # change to your test audio

    result = evaluate_answer(audio_file)

    print("\n==============================")
    print("CONFIDENCE SCORE :", result["confidence_score"])
    print("LEVEL            :", result["level"])
    print("==============================\n")

    print("TRANSCRIPT:")
    print(result["transcript"])

    print("\nFEATURES:")
    for k, v in result["features"].items():
        print(f"{k:15} : {v}")