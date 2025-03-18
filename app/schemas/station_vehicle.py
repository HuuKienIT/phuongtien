from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StationVehicleRequest(BaseModel):
    station_id: int
    vehicle_id: int
    charging_status: str
    departure_time: Optional[datetime] = None


class StationVehicleResponse(BaseModel):
    record_id: int
    station_id: int
    vehicle_id: int
    arrival_time: datetime
    departure_time: Optional[datetime] = None
    charging_status: str

    class Config:
        from_attributes = True