from sqlalchemy import Column, Integer, String,Enum
from app.db.base import Base

class UserRoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    restaurant_owner = "restaurant_owner"

class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

