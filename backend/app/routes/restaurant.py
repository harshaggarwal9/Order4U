from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant as restaurants
from app.schema.restaurant import RestaurantCreate, RestaurantUpdate
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_restaurant(payload: RestaurantCreate,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):

    if user.role not in ["admin", "restaurant_owner"]:

        raise HTTPException(status_code=403, detail="Not allowed")

    restaurant = restaurants(
        name=payload.name,
        address=payload.address
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


@router.get("/", status_code=status.HTTP_200_OK)
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(restaurants).all()


@router.put("/{restaurant_id}", status_code=status.HTTP_200_OK)
def update_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)):

    if user.role not in ["admin", "restaurant_owner"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    restaurant = db.query(restaurants).filter(restaurants.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if payload.name is not None:
        restaurant.name = payload.name

    if payload.address is not None:
        restaurant.address = payload.address

    db.commit()
    db.refresh(restaurant)

    return restaurant
