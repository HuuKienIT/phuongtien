from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VehicleRequest(BaseModel):
    licence_plate: str
    model: str
    battery_capacity: int
    current_station_id: Optional[int] = None
    total_km_driven: int
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_due: Optional[datetime] = None
    insurance_expiry_date: Optional[datetime] = None
    qr_code: Optional[str] = None

class VehicleResponse(BaseModel):
    id: int
    licence_plate: str
    model: str
    battery_capacity: int
    current_station_id: Optional[int] = None
    total_km_driven: int
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_due: Optional[datetime] = None
    insurance_expiry_date: Optional[datetime] = None
    qr_code: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
