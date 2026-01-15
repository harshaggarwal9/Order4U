from sqlalchemy import Column, Integer, ForeignKey, Float, String
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="PENDING_PAYMENT")