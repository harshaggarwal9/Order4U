from pydantic import BaseModel

class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str
      

class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str

    class Config:
        from_attributes = True
