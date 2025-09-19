from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer


from router import auth, chat
import models

from database import engine

app = FastAPI()

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["User Auth"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])



# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# fastapi dev main.py --host 0.0.0.0 --port 8000 --reload