from pydantic import BaseModel, Field

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
    
class voice_input(BaseModel):
    url: str = Field(min_length= 5)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://www.example.com/audio.wav"
            }
        }
    }
    
class ai_chat(BaseModel):
    message: str = Field(min_length= 1)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "How are you?"
            }
        }
    }