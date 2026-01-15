from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.base import Base

class order_items(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer,ForeignKey("orders.id", ondelete="CASCADE"),nullable=False,index=True)
    menu_item_id = Column(Integer,ForeignKey("menu_items.id"),nullable=False,index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
