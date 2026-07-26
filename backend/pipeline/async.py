import asyncio
from audio_feature_extractor import extract_confidence_score


async def extract_and_score(audio_file):
    # run the feature extractor + model
    result = extract_confidence_score(audio_file)
    return result["confidence_score"]


async def evaluate_answer(audio_file):

    confidence_score = await extract_and_score(audio_file)

    return {
        "confidence_score": confidence_score
    }