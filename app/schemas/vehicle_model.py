from typing import Optional
from pydantic import BaseModel


class VehicleModelRequest(BaseModel):
    model_name: str
    manufacture_year: int
    origin: Optional[str] = None
    vehicle_type: str
    engine_power: float
    battery_type: str
    battery_capacity: float
    nominal_battery_voltage: Optional[float] = None
    range_per_charge: Optional[float] = None
    vehicle_weight: Optional[float] = None
    max_load: Optional[float] = None
    braking_system: Optional[str] = None
    image_url: Optional[str] = None

class VehicleModelResponse(BaseModel):
    id: int
    model_name: str
    manufacture_year: int
    origin: Optional[str] = None
    vehicle_type: str
    engine_power: float
    battery_type: str
    battery_capacity: float
    nominal_battery_voltage: Optional[float] = None
    range_per_charge: Optional[float] = None
    vehicle_weight: Optional[float] = None
    max_load: Optional[float] = None
    braking_system: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
