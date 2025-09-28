from pydantic import BaseModel, Field
from typing import Optional
from fastapi import File, UploadFile, Form


class User(BaseModel):
    fullname: str = Field(min_length= 3)
    email: str = Field(min_length= 5)
    password: str = Field(min_length= 8)
    
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@gmail.com",
                "password": "password123"
            }
        }
    }
    
class Login(BaseModel):
    email: str = Field(min_length= 5)
    password: str = Field(min_length= 8)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe@gmail.com",
                "password": "password123"
            }
        }
    }
    
    
class Update_User(BaseModel):
    fullname: Optional[str] = Form(None)
    email: Optional[str] = Form(None)
    password: Optional[str] = Form(None)
    confirmPassword: Optional[str] = Form(None)
    profile_pic: UploadFile = File(...)


    model_config = {
        "json_schema_extra": {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@gmail.com",
                "confirmPassword": "password123",
                "password": "password123",
                # "profile_pic": "https://www.example.com/profile.jpg"
            }
        }
    }

    
class voice_input(BaseModel):
    url: str = Field(min_length= 5)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://www.example.com/audio.wav"
            }
        }
    }
    
class AIRequest(BaseModel):
    ai_response: str = Field(min_length= 1)
    
class ai_chat(BaseModel):
    message: str = Field(min_length= 1)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "How are you?"
            }
        }
    }
    
class encho_customize(BaseModel):
    voice: Optional[str] = Field(min_length=2)
    echo_language_output: Optional[str] = Field(min_length=2)