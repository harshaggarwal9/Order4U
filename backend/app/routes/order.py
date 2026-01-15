from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.order import Order as orders
from app.models.menu import menu_items
from app.models.order_items import order_items
from app.schema.order import OrderCreate
from starlette import status
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not payload.items or len(payload.items) == 0:
        raise HTTPException(status_code=400,detail="Order must contain at least one item")

    total_price = 0
    order_items_data = []

    for item in payload.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400,detail="Quantity must be greater than zero")

        menu = db.query(menu_items).filter(
            menu_items.id == item.menu_item_id,
            menu_items.restaurant_id == payload.restaurant_id).first()

        if not menu:
            raise HTTPException(status_code=404,detail=f"Menu item {item.menu_item_id} not found")

        item_total = menu.price * item.quantity
        total_price += item_total

        order_items_data.append({
            "menu_item_id": menu.id,
            "quantity": item.quantity,
            "price": menu.price
        })

    order = orders(
        user_id=user.id,
        restaurant_id=payload.restaurant_id,
        total_price=total_price,
        status="PENDING_PAYMENT"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_items_data:
        db.add(order_items(
            order_id=order.id,
            menu_item_id=item["menu_item_id"],
            quantity=item["quantity"],
            price=item["price"]
        ))

    db.commit()

    return {
        "order_id": order.id,
        "total_price": total_price,
        "status": order.status
    }


@router.get("/", status_code=status.HTTP_200_OK)
def get_user_orders(db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
   
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    orders_list = db.query(orders).filter(orders.user_id == user.id).all()

    return orders_list

@router.get("/{order_id}", status_code=status.HTTP_200_OK)
def get_order_by_id(order_id: int,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    order = db.query(orders).filter(orders.id == order_id,orders.user_id == user.id).first()

    if not order:
        raise HTTPException(status_code=404,detail="Order not found")

    return order
