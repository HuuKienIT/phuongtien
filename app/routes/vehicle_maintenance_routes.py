from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..data import get_db
from ..services import VehicleMaintenanceService
from ..schemas import VehicleMaintenanceRequest

vehicle_maintenance_router = APIRouter(prefix="/vehicle-maintenances", tags=["Vehicle Maintenances"])

@vehicle_maintenance_router.get("/{maintenance_id}")
async def get_maintenance_by_id(maintenance_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleMaintenanceService(db)
    return await service.get_maintenance_by_id(maintenance_id)


@vehicle_maintenance_router.get("/")
async def get_all_maintenances(page: int, page_size: int, db: AsyncSession = Depends(get_db)):
    service = VehicleMaintenanceService(db)
    return await service.get_all_maintenances(page, page_size)


@vehicle_maintenance_router.post("/")
async def create_maintenance(data: VehicleMaintenanceRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleMaintenanceService(db)
    return await service.create_maintenance(data.model_dump())


@vehicle_maintenance_router.put("/{maintenance_id}")
async def update_maintenance(maintenance_id: int, data: VehicleMaintenanceRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleMaintenanceService(db)
    return await service.update_maintenance(maintenance_id, data.model_dump())


@vehicle_maintenance_router.delete("/{maintenance_id}/soft")
async def delete_maintenance(maintenance_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleMaintenanceService(db)
    return await service.delete_maintenance(maintenance_id)
