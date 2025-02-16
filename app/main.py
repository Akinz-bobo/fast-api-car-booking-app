from fastapi import FastAPI
from app.db.session import init_db
from app.api.v1.endpoints import  users, slot, booking,auth



app = FastAPI(
    title="parking Application",
    description="API for Parking Application",
    version="1.0.0",   
)

# include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(slot.router, prefix="/api/v1/slots", tags=["slots"])
app.include_router(booking.router, prefix="/api/v1/booking", tags=["booking"])
@app.on_event("startup")

def startup():
    init_db()