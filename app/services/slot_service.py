from sqlalchemy.orm import Session
from app.db.repositories.slot_repository import SlotRepository
from app.schemas.slot import SlotCreate, SlotUpdate,SlotResponse
from app.utils.email import send_email

class SlotService:
    def __init__(self, db: Session):
        self.slot_repository = SlotRepository(db)

    def create_slot(self, slot_data: SlotCreate):
        existing_slot = self.slot_repository.get_slot_by_id(slot_data.slot_tag)
        if existing_slot:
            raise ValueError("slot with this id already exists")
        
        slot = self.slot_repository.create_slot(
            owner_id=slot_data.owner_id,
            price_per_hour=slot_data.price_per_hour,
            slot_tag=slot_data.slot_tag,
            address=slot_data.address,
            slot_capacity=slot_data.slot_capacity,
        )
        return slot

        
    def get_slot_by_id(self, slot_id: int):
            slot = self.slot_repository.get_slot_by_id(slot_id)
            if not slot:
                raise ValueError("slot not found")
            return slot
    
    def update_slot(self, slot_id: int, slot_data: SlotUpdate):
        slot = self.slot_repository.get_slot_by_id(slot_id)
        slot = self.slot_repository.update_slot(
            slot_id=slot_id,
            address=slot_data.address,
            slot_capacity=slot_data.slot_capacity,
            is_available=slot_data.is_available,
        )
        return slot
    
    def get_all_slots(self):
        slots = self.slot_repository.get_all_slots()
        return slots