import os
import json
import re
from typing import List
from google import genai
from models.schemas import AnswerItem, EvaluationItem

client = genai.Client()

class EvaluationService:
    def evaluate_answers(self, job_role: str, answers: List[AnswerItem]) -> List[EvaluationItem]:
        qa_text = "\n".join(
            [f"Q{a.question_id}: {a.question}\nA{a.question_id}: {a.answer}" for a in answers]
        )

        prompt = f"""You are a strict technical interviewer evaluating answers for a {job_role} position.

Evaluate each answer ONLY on technical correctness. Ignore grammar or communication style.

{qa_text}

Return ONLY a valid JSON array with one object per question:
[
  {{
    "question_id": "1",
    "is_correct": true or false,
    "correct_answer": "brief correct answer in 1-2 sentences"
  }},
  ...
]
No extra text outside the JSON."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

        data = json.loads(raw)

        results = []
        for item in data:
            results.append(EvaluationItem(
                question_id=str(item["question_id"]),
                is_correct=item["is_correct"],
                correct_answer=item["correct_answer"]
            ))
        return results

evaluation_service = EvaluationService()