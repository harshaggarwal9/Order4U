from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.menu import menu_items
from app.schema.menu import MenuItemCreate, MenuItemUpdate
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.post("/restaurant/{restaurant_id}", status_code=status.HTTP_201_CREATED)
def create_menu_item(restaurant_id: int,payload: MenuItemCreate,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):

    if user.role not in ["admin", "restaurant_owner"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    menu = menu_items(
        restaurant_id=restaurant_id,
        name=payload.name,
        description=payload.description,
        price=payload.price
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)

    return menu

@router.get("/restaurant/{restaurant_id}", status_code=status.HTTP_200_OK)
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(menu_items).filter(menu_items.restaurant_id == restaurant_id,menu_items.is_available == 1).all()


@router.put("/{menu_id}", status_code=status.HTTP_200_OK)
def update_menu_item(menu_id: int,payload: MenuItemUpdate,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    
    if user.role not in ["admin", "restaurant_owner"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    menu = db.query(menu_items).filter(menu_items.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if payload.name is not None:
        menu.name = payload.name

    if payload.description is not None:
        menu.description = payload.description

    if payload.price is not None:
        if payload.price <= 0:
            raise HTTPException(status_code=400, detail="Invalid price")
        menu.price = payload.price

    if payload.is_available is not None:
        menu.is_available = payload.is_available

    db.commit()
    db.refresh(menu)

    return menu
