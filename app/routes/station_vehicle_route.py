from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..data import get_db
from ..services import StationVehicleService
from ..schemas import StationVehicleRequest

station_vehicle_router = APIRouter(prefix="/station-vehicles", tags=["Station Vehicles"])

@station_vehicle_router.get("/{record_id}")
async def get_station_vehicle_by_id(record_id: int, db: AsyncSession = Depends(get_db)):
    service = StationVehicleService(db)
    return await service.get_station_vehicle_by_id(record_id)

@station_vehicle_router.get("/")
async def get_all_station_vehicles(page: int, page_size: int, db: AsyncSession = Depends(get_db)):
    service = StationVehicleService(db)
    return await service.get_all_station_vehicles(page, page_size)

@station_vehicle_router.post("/")
async def create_station_vehicle(data: StationVehicleRequest, db: AsyncSession = Depends(get_db)):
    service = StationVehicleService(db)
    return await service.create_station_vehicle(data.model_dump())

@station_vehicle_router.put("/{record_id}")
async def update_station_vehicle(record_id: int, data: StationVehicleRequest, db: AsyncSession = Depends(get_db)):
    service = StationVehicleService(db)
    return await service.update_station_vehicle(record_id, data.model_dump())

@station_vehicle_router.delete("/{record_id}/soft")
async def delete_station_vehicle(record_id: int, db: AsyncSession = Depends(get_db)):
    service = StationVehicleService(db)
    return await service.delete_station_vehicle(record_id)