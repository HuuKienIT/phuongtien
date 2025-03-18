from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VehicleInsuranceRequest(BaseModel):
    vehicle_id: int
    provider_name: str
    policy_number: str
    start_date: datetime
    expiry_date: datetime
    coverage_details: Optional[str] = None
    status: str

class VehicleInsuranceResponse(BaseModel):
    id: int
    vehicle_id: int
    provider_name: str
    policy_number: str
    start_date: datetime
    expiry_date: datetime
    coverage_details: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
