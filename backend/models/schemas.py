from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    id: str
    question: str

class AnswerItem(BaseModel):
    question_id: str
    question: str
    answer: str

class InterviewEvaluationRequest(BaseModel):
    session_id: str
    job_role: str
    answers: List[AnswerItem]

class EvaluationItem(BaseModel):
    question_id: str
    is_correct: bool
    correct_answer: str

class EvaluationResult(BaseModel):
    score: int
    total: int
    feedback: List[EvaluationItem]


class AudioFeatures(BaseModel):
    pitch_mean: float
    pitch_var: float
    speech_rate: float
    pause_count: int
    avg_pause: float
    energy_mean: float
    jitter: float
    shimmer: float
    filler_words: int


class AudioEvaluationResult(BaseModel):
    confidence_score: float
    level: str
    transcript: str
    features: AudioFeatures

class ResumeUploadResponse(BaseModel):
    session_id: str
    questions: List[Question]