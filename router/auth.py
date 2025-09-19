from fastapi import APIRouter, Depends, HTTPException, status
import schema
import database
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timedelta
from models import User
from utils.access_token import create_access_token

# auth
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bycrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code = status.HTTP_201_CREATED)
async def register(create_user: schema.User, db: db_dependency):
    # check if user already exists
    user = db.query(User).filter(User.email == create_user.email).first()
    
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # hash password
    hashed_password = bycrypt.hash(create_user.password)
    
    # create user object
    user_model = User(
        fullname=create_user.fullname,
        email=create_user.email,
        password= hashed_password
    )
    
    
   
    
    # add user to database
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    
    
    user = {
        "id": user_model.id,
        # "fullname": user_model.fullname,
        # "email": user_model.email
    }
    
     # create access token
    token = create_access_token(fullname=user_model.fullname, user_id=user_model.id) # type: ignore
    return {"message": "User created successfully", "access_token": token, "token_type": "bearer", "user": user} 
    


@router.post("/login", status_code = status.HTTP_200_OK)
async def login(db: db_dependency, login_request: schema.Login):
    
    # check if user exists
    user = db.query(User).filter(User.email == login_request.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    
    # verify password
    if not bycrypt.verify(login_request.password, user.password): # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
     
    # create access token
    token = create_access_token(fullname=user.fullname, user_id=user.id) # type: ignore
    
    user = {
        "id": user.id,
        # "fullname": user.fullname,
        # "email": user.email
    }
    
    return { "message": "Login successful", "access_token": token, "token_type": "bearer", "user": user}

@router.get("/user/{id}", status_code = status.HTTP_200_OK)
async def get_user(id: int, db: db_dependency):
    # check if user exists
    user = db.query(User).filter(User.id == id).first()
     
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
     
    userData = {
        "id": user.id,
        "fullname": user.fullname,
        "email": user.email 
    }
     
    return userData