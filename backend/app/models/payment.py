import enum
from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from app.db.base import Base
import enum

class PaymentStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PaymentMethodEnum(str, enum.Enum):
    UPI = "UPI"
    CARD = "CARD"
    CASH = "CASH"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethodEnum, name="payment_method_enum"),nullable=False)
    status = Column(Enum(PaymentStatusEnum, name="payment_status_enum"),default=PaymentStatusEnum.PENDING,nullable=False)

