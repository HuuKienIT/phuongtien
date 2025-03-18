from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..data import get_db
from ..services import VehicleRegistrationService
from ..schemas import VehicleRegistrationRequest

vehicle_registration_router = APIRouter(prefix="/vehicle-registrations", tags=["Vehicle registrations"])

@vehicle_registration_router.get("/{registration_id}")
async def get_registration_by_id(registration_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleRegistrationService(db)
    return await service.get_registration_by_id(registration_id)


@vehicle_registration_router.get("/")
async def get_all_registrations(page: int, page_size: int, db: AsyncSession = Depends(get_db)):
    service = VehicleRegistrationService(db)
    return await service.get_all_registrations(page, page_size)

@vehicle_registration_router.get("/vehicle/{vehicle_id}")
async def get_registration_by_vehicle_id(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleRegistrationService(db)
    return await service.get_registrations_by_vehicle_id(vehicle_id)

@vehicle_registration_router.post("/")
async def create_registration(data: VehicleRegistrationRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleRegistrationService(db)
    return await service.create_registration(data.model_dump())


@vehicle_registration_router.put("/{registration_id}")
async def update_registration(registration_id: int, data: VehicleRegistrationRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleRegistrationService(db)
    return await service.update_registration(registration_id, data.model_dump())

@vehicle_registration_router.delete("/{registration_id}/soft")
async def delete_registration(registration_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleRegistrationService(db)
    return await service.delete_registration(registration_id)
