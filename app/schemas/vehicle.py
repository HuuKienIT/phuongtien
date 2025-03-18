from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VehicleRequest(BaseModel):
    licence_plate: str
    vehicle_model_id: int
    color: Optional[str] = None
    current_battery_capacity: float
    current_station_id: Optional[int] = None
    total_km_driven: float
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_due: Optional[datetime] = None
    insurance_expiry_date: Optional[datetime] = None
    qr_code: Optional[str] = None
    status: str

class VehicleResponse(BaseModel):
    id: int
    licence_plate: str
    vehicle_model_id: int
    color: Optional[str] = None
    current_battery_capacity: float
    current_station_id: Optional[int] = None
    total_km_driven: float
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_due: Optional[datetime] = None
    insurance_expiry_date: Optional[datetime] = None
    qr_code: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
