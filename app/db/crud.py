# CRUD Create, Read, Update, Delete

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.user import UserCreate
from app.db.models import User


# Initialize the Password-based CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    """Get user by username."""
    print("get_user_by_username")
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Get user by username."""
    print("get_user_by_email")
    return db.query(User).filter(User.email == email).first()


def verify_password(plain_password: str, hashed_password: str):
    """Verify password."""
    print("veryfy_password")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Hash the password."""
    print("hash_password")
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    print("create_user")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id
