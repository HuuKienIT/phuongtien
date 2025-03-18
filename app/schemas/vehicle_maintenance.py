from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VehicleMaintenanceRequest(BaseModel):
    vehicle_id: int
    maintenance_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    cost: int
    maintenance_details: Optional[str] = None


class VehicleMaintenanceResponse(BaseModel):
    maintenance_id: int
    vehicle_id: int
    maintenance_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    cost: int
    maintenance_details: Optional[str] = None

    class Config:
        from_attributes = True
