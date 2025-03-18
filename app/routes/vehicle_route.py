from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..data import get_db
from ..services import VehicleService
from ..schemas import VehicleRequest

vehicle_router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@vehicle_router.get("/{vehicle_id}")
async def get_vehicle_by_id(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleService(db)
    return await service.get_vehicle_by_id(vehicle_id)


@vehicle_router.get("/")
async def get_all_vehicles(page: int, page_size: int, db: AsyncSession = Depends(get_db)):
    service = VehicleService(db)
    return await service.get_all_vehicles(page, page_size)


@vehicle_router.post("/")
async def create_vehicle(data: VehicleRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleService(db)
    return await service.create_vehicle(data.model_dump())


@vehicle_router.put("/{vehicle_id}")
async def update_vehicle(vehicle_id: int, data: VehicleRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleService(db)
    return await service.update_vehicle(vehicle_id, data.model_dump())


@vehicle_router.delete("/{vehicle_id}/soft")
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleService(db)
    return await service.delete_vehicle(vehicle_id)