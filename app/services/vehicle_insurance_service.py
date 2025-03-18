from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils import ApiResponse
from ..unit_of_work import UnitOfWork
from ..schemas import VehicleInsuranceResponse

class VehicleInsuranceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.uow = UnitOfWork(db)

    async def get_insurance_by_id(self, insurance_id: int) -> ApiResponse[VehicleInsuranceResponse]:
        async with self.uow as uow:
            insurance = await uow.vehicle_insurance_repository.get_by(filters={"id": insurance_id})
            if not insurance:
                raise HTTPException(status_code=404, detail="Insurance not found")
            return ApiResponse(status=200, message="Insurance found",
                               data=VehicleInsuranceResponse.model_validate(insurance))

    async def get_all_insurances(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.vehicle_insurance_repository.get_all(page=page, page_size=page_size)
            return ApiResponse(
                status=200,
                message="Insurances retrieved",
                data={
                    "insurances": [VehicleInsuranceResponse.model_validate(insurance) for insurance in result["items"]],
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def get_insurances_by_vehicle_id(self, vehicle_id: int) -> ApiResponse[list]:
        async with self.uow as uow:
            result = await uow.vehicle_insurance_repository.get_all(filters={"vehicle_id": vehicle_id})
            return ApiResponse(
                status=200,
                message="Insurances retrieved",
                data=[VehicleInsuranceResponse.model_validate(insurance) for insurance in result["items"]]
            )

    async def create_insurance(self, data: dict) -> ApiResponse[VehicleInsuranceResponse]:
        async with self.uow as uow:
            insurance = await uow.vehicle_insurance_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Insurance created",
                               data=VehicleInsuranceResponse.model_validate(insurance))

    async def update_insurance(self, insurance_id: int, data: dict) -> ApiResponse[VehicleInsuranceResponse]:
        async with self.uow as uow:
            insurance = await uow.vehicle_insurance_repository.get_by(filters={"id": insurance_id})
            if not insurance:
                raise HTTPException(status_code=404, detail="Insurance not found")
            updated_insurance = await uow.vehicle_insurance_repository.update(insurance, data)
            await uow.commit()
            return ApiResponse(status=200, message="Insurance updated",
                               data=VehicleInsuranceResponse.model_validate(updated_insurance))

    async def delete_insurance(self, insurance_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            insurance = await uow.vehicle_insurance_repository.get_by(filters={"id": insurance_id})
            if not insurance:
                raise HTTPException(status_code=404, detail="Insurance not found")
            await uow.vehicle_insurance_repository.soft_delete(insurance)
            await uow.commit()
            return ApiResponse(status=200, message="Insurance deleted", data=None)
