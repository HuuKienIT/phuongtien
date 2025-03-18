from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema
class VehicleInsuranceRequest(BaseModel):
    vehicle_id: int
    provider_name: str
    policy_number: str
    start_date: datetime
    expiry_date: datetime
    coverage_details: Optional[str] = None


class VehicleInsuranceResponse(BaseModel):
    insurance_id: int
    vehicle_id: int
    provider_name: str
    policy_number: str
    start_date: datetime
    expiry_date: datetime
    coverage_details: Optional[str] = None

    class Config:
        from_attributes = True
