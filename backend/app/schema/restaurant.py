from pydantic import BaseModel, Field
from typing import Optional

class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2,max_length=100)
    address: str = Field(min_length=5,max_length=255)

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(default=None,min_length=2,max_length=100)
    address: Optional[str] = Field(default=None,min_length=5,max_length=255)