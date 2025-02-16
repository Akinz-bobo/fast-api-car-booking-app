from sqlalchemy.orm import Session
from app.db.models.booking import Booking

class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_booking(self, user_id: int, slot_id: int, price: int) -> Booking:
        booking = Booking( user_id=user_id, slot_id=slot_id, price=price)        
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update_booking(self, booking_id: int, price: int = None, slot_id: int = None) -> Booking:
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return None  # Handle case where booking doesn't exist.

        if price is not None:
            booking.price = price
        if slot_id is not None:
            booking.slot_id = slot_id

        self.db.commit()  # Save changes to the database.
        self.db.refresh(booking)  # Refresh to get updated data.
        return booking


    def get_booking_by_id(self, booking_id: int) -> Booking:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()
        
    def get_all_bookings(self):
        return self.db.query(Booking).all()