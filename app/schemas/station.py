from typing import Optional
from pydantic import BaseModel

class StationRequest(BaseModel):
    name: str
    location: Optional[str] = None
    latitude: int
    longitude: int
    total_slots: int
    available_vehicles: int
    charging_capacity: int
    status: str


class StationResponse(BaseModel):
    id: int
    name: str
    location: Optional[str] = None
    latitude: int
    longitude: int
    total_slots: int
    available_vehicles: int
    charging_capacity: int
    status: str

    class Config:
        from_attributes = True