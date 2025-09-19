from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# location of the database file
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Standout070801?@127.0.0.1:3306/echo-voice-assistant"


# create engine to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# create a local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for declarative models
Base = declarative_base()