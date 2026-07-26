import uuid
from typing import List, Dict, Any
from models.schemas import Question, ResumeUploadResponse, EvaluationItem, EvaluationResult

class EvaluationService:
    @staticmethod
    def create_session(questions_data: List[Dict[str, Any]]) -> ResumeUploadResponse:
        session_id = str(uuid.uuid4())
        questions = [Question(id=q['id'], question=q['question']) for q in questions_data]
        return ResumeUploadResponse(session_id=session_id, questions=questions)

    @staticmethod
    def calculate_results(evaluations_data: List[Dict[str, Any]]) -> EvaluationResult:
        eval_items = []
        correct_count = 0
        
        for e in evaluations_data:
            eval_items.append(EvaluationItem(
                question_id=e['question_id'],
                is_correct=e['is_correct'],
                correct_answer=e['correct_answer']
            ))
            if e['is_correct']:
                correct_count += 1
                
        total = len(evaluations_data)
        score = int((correct_count / total) * 100) if total > 0 else 0
        
        return EvaluationResult(
            score=score,
            total=total,
            feedback=eval_items
        )
