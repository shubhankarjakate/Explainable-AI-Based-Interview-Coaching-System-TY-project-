from fastapi import APIRouter, HTTPException
from models.schemas import InterviewEvaluationRequest, EvaluationResult
from services.llm_service import LLMService
from services.evaluation_service import EvaluationService

router = APIRouter(prefix="/interview", tags=["interview"])
llm_service = LLMService()

@router.post("/evaluate", response_model=EvaluationResult)
async def evaluate_interview(request: InterviewEvaluationRequest):
    try:
        # Format the qa pairs for LLM
        qa_pairs = [
            {
                "question_id": item.question_id,
                "question": item.question,
                "answer": item.answer
            }
            for item in request.answers
        ]
        
        evaluations_data = llm_service.evaluate_answers(request.job_role, qa_pairs)
        
        return EvaluationService.calculate_results(evaluations_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))