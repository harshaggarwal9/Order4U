from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.order import Order as orders
from app.models.payment import Payment as payments
from app.schema.payment import PaymentCreate
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.payment import PaymentStatusEnum

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate,db: Session = Depends(get_db),user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    order = db.query(orders).filter(orders.id == payload.order_id,orders.user_id == user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "PENDING_PAYMENT":
        raise HTTPException(status_code=400, detail="Order already paid or cancelled")

    payment = payments(
        order_id=order.id,
        user_id=user.id,
        amount=order.total_price,
        payment_method=payload.payment_method,   
        status=PaymentStatusEnum.COMPLETED      
    )

    order.status = "CONFIRMED"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "payment_id": payment.id,
        "order_id": order.id,
        "amount": payment.amount,
        "status": payment.status
    }


@router.get("/", status_code=status.HTTP_200_OK)
def get_user_payments(db: Session = Depends(get_db),user: dict = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return db.query(payments).filter(payments.user_id == user.id).all()


@router.put("/{order_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_order(order_id: int,db: Session = Depends(get_db),user = Depends(get_current_user)):

    order = db.query(orders).filter( orders.id == order_id, orders.user_id == user.id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.status != "PENDING_PAYMENT":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Order cannot be cancelled after payment")

    order.status = "CANCELLED"
    db.commit()

    return {
        "message": "Order cancelled successfully",
        "order_id": order.id,
        "status": order.status
    }

