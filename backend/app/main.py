from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routes import auth
from app.routes import restaurant
from app.routes import menu
from app.routes import order
from app.routes import payment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(restaurant.router, tags=["Restaurants"])
app.include_router(menu.router,  tags=["Menu"])
app.include_router(order.router,tags=["Orders"])
app.include_router(payment.router,tags=["Payments"])

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Food Delivery API is running "}
