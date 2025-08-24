from sqlalchemy.orm import Session
from sqlalchemy.future import select
from db.models import User
from schema.user import UserCreate
import uuid


def get_user_by_email(db: Session, email: str):
    result = db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


def get_user(db: Session, user_id: str):
    result = db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        id=uuid.uuid4(),
        name=user.name,
        email=user.email,
        password_hash=user.password,
        is_verified=True,
        api_key=user.api_key,
        account_type=user.account_type

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user