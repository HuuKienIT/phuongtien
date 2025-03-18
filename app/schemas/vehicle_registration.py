from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VehicleRegistrationRequest(BaseModel):
    vehicle_id: int
    registration_number: str
    agency: str
    start_date: datetime
    end_date: datetime
    status: str
    note: Optional[str] = None

class VehicleRegistrationResponse(BaseModel):
    id: int
    vehicle_id: int
    registration_number: str
    agency: str
    start_date: datetime
    end_date: datetime
    status: str
    note: Optional[str] = None

    class Config:
        from_attributes = True