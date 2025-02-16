from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.booking_service import BookingService
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse



router = APIRouter()

@router.post("/", response_model=BookingResponse, summary="Create a new booking")
def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    booking_service = BookingService(db)
    return booking_service.create_booking(booking_data)

    # Get all bookings
@router.get("/", response_model=list[BookingResponse], summary="Get all bookings") 
def get_all_bookings(db: Session = Depends(get_db)):
    booking_service = BookingService(db)
    return booking_service.get_all_bookings()

    # update bookings
@router.put("/{slot_id}", response_model=BookingResponse, summary="update the booking")
def update_booking(booking_id: int, booking_data: BookingUpdate, db:Session = Depends(get_db)):
    booking_service =BookingService(db)
    return booking_service.update_booking(booking_id, booking_data)

    # get booking by id
@router.get("/{booking_id}",response_model=BookingResponse, summary="Get booking by id")
def get_booking(booking_id: int, db: Session = Depends(get_db)) :
    booking_service = BookingService(db)
    return booking_service.get_booking_by_id(booking_id)
    