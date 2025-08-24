from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import get_db
from db.models import Base
from db.session import engine

from api.routes import auth, user

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Create the DB tables (if not using Alembic yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz Platform", version="1.0.0")



# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Quiz Platform API"}