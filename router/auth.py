from fastapi import APIRouter, Depends, HTTPException, status, Path, UploadFile, File, Form
import schema
import database
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import datetime, timedelta
from models import User
from utils.access_token import create_access_token
from utils.get_current_user import get_current_user
import os
from dotenv import load_dotenv
load_dotenv()

# cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api
# from cloud import api_key, api_secret, cloud_name

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
user_dependency = Annotated[dict, Depends(get_current_user)]

# cloudinary config
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure = True
)
# cloudinary.config( 
#   cloud_name = cloud_name[0], 
#   api_key = api_key[0],
#   api_secret = api_secret[0],
#   secure = True
# )


@router.post("/register", status_code = status.HTTP_201_CREATED)
async def register(create_user: schema.User, db: db_dependency):
    # check if user already exists
    try:
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
    
    except HTTPException:
        # ✅ re-raise known HTTP exceptions as they are
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}"
        )
    
    

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(db: db_dependency, login_request: schema.Login):
    try:
        # check if user exists
        user = db.query(User).filter(User.email == login_request.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # verify password
        if not bycrypt.verify(login_request.password, user.password):  # type: ignore
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        # create access token
        token = create_access_token(fullname=user.fullname, user_id=user.id)  # type: ignore

        return {
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {"id": user.id}
        }

    except HTTPException:
        # ✅ re-raise known HTTP exceptions as they are
        raise
    except Exception as e:
        # ❗ catch unexpected errors only
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}"
        )

        

@router.get("/user/{id}", status_code = status.HTTP_200_OK)
async def get_user(id: int, db: db_dependency):
    try:
        # check if user exists
        user = db.query(User).filter(User.id == id).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        userData = {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "profile_pic": user.profile_pic,
        }
        
        return userData
    
    except HTTPException:
        # ✅ re-raise known HTTP exceptions as they are
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}"
        )

@router.patch("/user/{id}", status_code=status.HTTP_200_OK)
async def update_user_infor(
    db: db_dependency,
    id: int = Path(ge=1),
    fullname: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    confirmPassword: Optional[str] = Form(None),
    profile_pic: UploadFile = File(None),
):
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update fullname
        if fullname:
            user.fullname = fullname # type: ignore

        # Update email with uniqueness check
        if email:
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user and existing_user.id != user.id: # type: ignore
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = email # type: ignore

        # Update password
        if password:
            if not confirmPassword or password != confirmPassword:
                raise HTTPException(status_code=400, detail="Passwords do not match")
            user.password = bycrypt.hash(password) # type: ignore

        # Upload profile picture
        if profile_pic:
            result = cloudinary.uploader.upload(
                profile_pic.file,
                folder=f"echo-user-pic",
                public_id=f"user_{user.id}",
                overwrite=True,
                resource_type="image"
            )
            user.profile_pic = result["secure_url"]

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User profile updated successfully",
            "user": {
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email,
                "profile_pic": user.profile_pic,
            }
        }
    
    except HTTPException:
        # ✅ re-raise known HTTP exceptions as they are
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}"
        )
