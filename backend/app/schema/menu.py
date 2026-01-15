from pydantic import BaseModel
from typing import Optional

class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: Optional[int] = 1

class MenuItemRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    is_available: int
    
    class Config:from_attributes = True

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[int] = None