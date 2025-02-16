
from sqlalchemy.orm import Session
from app.db.models.slot import Slot

class SlotRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_slot(self,owner_id:int, price_per_hour:int, slot_capacity:str, address:str, slot_tag:str ) -> Slot:
        slot = Slot(address=address, price_per_hour=price_per_hour,owner_id=owner_id, slot_capacity=slot_capacity, slot_tag=slot_tag)
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def get_slot_by_tag(self, slot_tag: str) -> Slot:
        return self.db.query(Slot).filter(Slot.id == slot_tag).first()
    def get_slot_by_tag(self, slot_tag: str) -> Slot:
        return self.db.query(Slot).filter(Slot.slot_tag == slot_tag).first()
    
    def get_all_slots(self):
        return self.db.query(Slot).all()
    
    def update_slot(self, slot_id: str, owner_id:int = None, price_per_hour:int = None, slot_capacity:str = None, address:str = None, is_available:bool=True) -> Slot:
        slot = self.get_slot_by_id(slot_id)
        if owner_id:
            slot.owner_id = owner_id
        if price_per_hour:
            slot.price_per_hour = price_per_hour
        if slot_capacity:
            slot.slot_capacity = slot_capacity
        if address:
            slot.address = address
        if is_available:
            slot.is_available = is_available
        self.db.commit()
        self.db.refresh(slot)
        return slot