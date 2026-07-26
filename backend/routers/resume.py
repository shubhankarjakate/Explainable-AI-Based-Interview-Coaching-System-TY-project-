from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.pdf_service import PDFService
from services.llm_service import LLMService
from services.evaluation_service import EvaluationService
from models.schemas import ResumeUploadResponse

router = APIRouter(prefix="/resume", tags=["resume"])
llm_service = LLMService()

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    job_role: str = Form(...),
    que_level:str = 'easy'
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        file_bytes = await file.read()
        resume_text = PDFService.extract_text_from_pdf(file_bytes)
        
        # Generate questions
        questions_data = llm_service.generate_questions(resume_text, job_role,que_level)
        
        # Create session
        return EvaluationService.create_session(questions_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))