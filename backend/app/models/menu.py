from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.base import Base

class menu_items(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    is_available = Column(Integer, default=1) 
