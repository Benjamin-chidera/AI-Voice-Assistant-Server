from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from faster_whisper import WhisperModel
import database
from sqlalchemy.orm import Session
from typing import Annotated
from utils.get_current_user import get_current_user
import io

# speak to llm
from utils.llm_communication import speak_to_llm

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Load model once globally
model = WhisperModel("medium")

@router.post("/communicate", status_code=status.HTTP_201_CREATED)
async def communicate(
    db: db_dependency,
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Use file.file which is a file-like object (stream) without saving to disk
    audio_stream = file.file  # type: ignore 

    # Faster Whisper expects a path, numpy array, or file-like object with read()
    segments, _ = model.transcribe(audio_stream)
    text = " ".join([seg.text for seg in segments])

    print("Transcribed text:", text)
    
    await speak_to_llm(text)

    return {"text": text}
