from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.slot_service import SlotService
from app.schemas.slot import SlotCreate, SlotUpdate, SlotResponse
router = APIRouter() 

@router.post("/", response_model=SlotResponse, summary="Create a new parking slot")
def create_slot(slot_data: SlotCreate, db: Session = Depends(get_db)):
    slot_service = SlotService(db)
    return slot_service.create_slot(slot_data)


@router.get("/", response_model=list[SlotResponse], summary="Get all parking slots")
def get_all_slots(db: Session = Depends(get_db)):
    slot_service = SlotService(db)
    return slot_service.get_all_slots()

@router.put("/{slot_id}", response_model=SlotResponse, summary="Update a parking slot")
def update_slot(slot_id: int, slot_data: SlotUpdate, db: Session = Depends(get_db)):
    slot_service = SlotService(db)
    return slot_service.update_slot(slot_id, slot_data)

@router.get("/{slot_id}",response_model=SlotResponse, summary="Get a parking slot by id")

def get_slot(slot_id: int, db: Session = Depends(get_db)):
    slot_service = SlotService(db)
    return slot_service.get_slot_by_id(slot_id)