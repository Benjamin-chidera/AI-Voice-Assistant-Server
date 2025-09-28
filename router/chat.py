from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from faster_whisper import WhisperModel
import database
from sqlalchemy.orm import Session
from typing import Annotated
from utils.get_current_user import get_current_user
import io
from models import User
import schema

# speak to llm
from utils.llm_communication import speak_to_llm, chat_llm, audio_stream_fn

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
    
    user_voice = db.query(User).filter(User.id == user["id"]).first()
    
    print("User voice:", user_voice.voice) # type: ignore

    # Use file.file which is a file-like object (stream) without saving to disk
    audio_stream = file.file  # type: ignore 
 
    # Faster Whisper expects a path, numpy array, or file-like object with read()
    segments, _ = model.transcribe(audio_stream)
    user_text = " ".join([seg.text for seg in segments])

    # print("Transcribed user_text:", user_text)    
    ai_response = await speak_to_llm(user_text, voice=user_voice.voice, language=user_voice.echo_language_output) # type: ignore

    return {"user_text": user_text,
            "ai_response": ai_response,
            }

# @router.post("/stream_communicate", status_code=status.HTTP_201_CREATED)
# async def stream_communicate(
#     db: db_dependency,
#     request: schema.AIRequest,
#     user: dict = Depends(get_current_user)
# ):
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
#     user_voice = db.query(User).filter(User.id == user["id"]).first()
#     print("User voice:", user_voice.voice)  # type: ignore

#     return StreamingResponse(
#         audio_stream_fn(voice=user_voice.voice, ai_response=request.ai_response), # type: ignore
#         media_type="audio/mpeg"
#     )

@router.post("/chat_with_ai", status_code=status.HTTP_201_CREATED)
async def chat_with_llm(
    db: db_dependency,
    message: schema.ai_chat,
    user: dict = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    echo_language_output = db.query(User).filter(User.id == user["id"]).first()
        
    ai_chat = await chat_llm(message.message, language=echo_language_output.echo_language_output) # type: ignore
    
    print("AI chat response:", ai_chat)
    print("User chat message:", message.message)
    
    return {
        "ai_chat": ai_chat,
        "user_chat": message.message
    }