from typing import Optional
from pydantic import BaseModel

class StationRequest(BaseModel):
    name: str
    location: Optional[str] = None
    latitude: float
    longitude: float
    total_slots: int
    total_vehicles: int
    available_vehicles: int
    charging_capacity: int
    status: str

class StationResponse(BaseModel):
    id: int
    name: str
    location: Optional[str] = None
    latitude: float
    longitude: float
    total_slots: int
    total_vehicles: int
    available_vehicles: int
    charging_capacity: int
    status: str

    class Config:
        from_attributes = True