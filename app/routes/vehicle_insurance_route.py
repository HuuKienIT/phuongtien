from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..data import get_db
from ..services import VehicleInsuranceService
from ..schemas import VehicleInsuranceRequest

vehicle_insurance_router = APIRouter(prefix="/vehicle-insurances", tags=["Vehicle Insurances"])

@vehicle_insurance_router.get("/{insurance_id}")
async def get_insurance_by_id(insurance_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleInsuranceService(db)
    return await service.get_insurance_by_id(insurance_id)


@vehicle_insurance_router.get("/")
async def get_all_insurances(page: int, page_size: int, db: AsyncSession = Depends(get_db)):
    service = VehicleInsuranceService(db)
    return await service.get_all_insurances(page, page_size)


@vehicle_insurance_router.post("/")
async def create_insurance(data: VehicleInsuranceRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleInsuranceService(db)
    return await service.create_insurance(data.model_dump())


@vehicle_insurance_router.put("/{insurance_id}")
async def update_insurance(insurance_id: int, data: VehicleInsuranceRequest, db: AsyncSession = Depends(get_db)):
    service = VehicleInsuranceService(db)
    return await service.update_insurance(insurance_id, data.model_dump())


@vehicle_insurance_router.delete("/{insurance_id}/soft")
async def delete_insurance(insurance_id: int, db: AsyncSession = Depends(get_db)):
    service = VehicleInsuranceService(db)
    return await service.delete_insurance(insurance_id)
