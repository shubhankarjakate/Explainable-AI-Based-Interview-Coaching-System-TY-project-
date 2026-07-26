import dotenv
dotenv.load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import resume, interview, asr, audio_eval

app = FastAPI(title="Interview Prep AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(interview.router)
app.include_router(asr.router)
app.include_router(audio_eval.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Interview Prep AI API"}