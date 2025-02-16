


from pydantic import BaseModel, Field
from typing import Optional


class SlotBase(BaseModel):
    """
    Shared properties for parking slots.
    """
    owner_id: int = Field(..., description="Unique identifier of the slot owner.")

class SlotCreate(SlotBase):
    """
    Properties required for creating a new parking slot.
    """
    price_per_hour: int = Field(..., description="Price per hour of the parking slot.")
    address: str = Field(..., description="Address of the parking slot.")
    slot_capacity: int  = Field(..., description="Capacity of the parking slot.")
    slot_tag: str = Field(..., description="Tag of the parking slot.")
    
   
class SlotUpdate(BaseModel):
    """
    Properties for updating a parking slot.
    """
    is_available: Optional[bool] = Field(None, description="Update the availability of the slot.")
    price_per_hour: Optional[int] = Field(None, description="Update the price per hour of the slot.")
    address: Optional[str] = Field(None, description="Update the address of the slot.")
    


class SlotResponse(SlotBase):
    """
    Properties returned in response to slot-related endpoints.
    """
    id: int = Field(..., description="Unique identifier of the parking slot.")
    
    class Config:
        from_attributes = True