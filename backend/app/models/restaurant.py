from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    cuisine_type = Column(String)

