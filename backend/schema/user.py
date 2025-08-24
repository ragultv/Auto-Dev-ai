from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    api_key: str | None = None

class UserCreateInternal(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    password: str
    api_key: str | None = None
    is_verified: bool = True
    account_type: str = "free"  # free, premium, enterprise
    created_at: datetime
    updated_at: datetime | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    class Config:
        from_attributes = True

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str
    class Config:
        from_attributes = True

class UserSessionResponse(BaseModel):
    session_id: str
    score: float
    topic: str
    num_questions: int
    time_taken :str
    difficulty: str

class UserStatsResponse(BaseModel):
    total_quiz: int
    best_score: float

class UsernameAvailability(BaseModel):
    available: bool

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    otp: str

class EmailSchema(BaseModel):
    email: str