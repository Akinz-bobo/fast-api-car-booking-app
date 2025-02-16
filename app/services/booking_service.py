from sqlalchemy.orm import Session
from app.db.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.utils.email import send_email


class BookingService:
    def __init__(self, db: Session):
        self.booking_repository = BookingRepository(db)
# create a new booking.
    def create_booking(self, booking_data: BookingCreate):
        existing_booking = self.booking_repository.get_booking_by_id(booking_data.booking_id)
        if existing_booking:
            raise ValueError("booking with this id already exist")

        booking = self.booking_repository.create_booking(
            user_id=booking_data.user_id,
            slot_id=booking_data.slot_id,
            price=booking_data.price,
        ) 
        return booking      
    
    def get_booking_by_id(self, booking_id: int):
            booking = self.booking_repository.get_slot_by_id(booking_id)
            if not booking:
                raise ValueError("booking not found")
            return 
    
    def update_booking(self, booking_id: int, booking_data: BookingUpdate):
        booking = self.booking_repository.get_booking_by_id(booking_id)
        booking = self.booking_repository.update_booking(
            price=booking_data.price,
            slot_id=booking_data.slot_id,
        )
        return booking
    def get_all_booking(self):
        booking = self.booking_repository.get_all_booking()
        return booking
    