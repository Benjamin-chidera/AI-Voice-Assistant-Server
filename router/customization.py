from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Path
from faster_whisper import WhisperModel
import database
from sqlalchemy.orm import Session
from typing import Annotated
from utils.get_current_user import get_current_user
import io
from models import User
import schema

# speak to llm
from utils.llm_communication import speak_to_llm, chat_llm

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.patch("/customize/{id}", status_code=status.HTTP_200_OK)
async def customize_echo(user:user_dependency, db: db_dependency, echo_request: schema.encho_customize, id: int = Path(ge=1)):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_id = db.query(User).filter(User.id == id).first()
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #  update customization
    if echo_request.voice:
        user_id.voice = echo_request.voice # type: ignore
        
    if echo_request.echo_language_output: 
        user_id.echo_language_output = echo_request.echo_language_output # type: ignore
        
    db.commit()
    db.refresh(user_id)
    
    return {"message": "Customization updated successfully", "voice": user_id.voice, "echo_language_output": user_id.echo_language_output} # type: ignore