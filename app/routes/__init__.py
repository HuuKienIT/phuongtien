from .station_routes import station_router
from .station_vehicle_route import station_vehicle_router
from .vehicle_route import vehicle_router
from .vehicle_insurance_route import vehicle_insurance_router
from .vehicle_maintenance_routes import vehicle_maintenance_router

__all__ = ['station_router', 'station_vehicle_router', 'vehicle_router',
           'vehicle_insurance_router', 'vehicle_maintenance_router']