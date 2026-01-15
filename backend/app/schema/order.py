from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int
    

class OrderCreate(BaseModel):
    items: List[OrderItem]
    restaurant_id: int

