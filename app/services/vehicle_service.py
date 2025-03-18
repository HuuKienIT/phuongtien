from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import ApiResponse
from ..unit_of_work import UnitOfWork
from ..schemas import VehicleResponse

class VehicleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.uow = UnitOfWork(db)

    async def get_vehicle_by_id(self, vehicle_id: int) -> ApiResponse[VehicleResponse]:
        async with self.uow as uow:
            vehicle = await uow.vehicle_repository.get_by(id=vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")
            return ApiResponse(status=200, message="Vehicle found", data=VehicleResponse.model_validate(vehicle))

    async def get_all_vehicles(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.vehicle_repository.get_all(page, page_size)

            return ApiResponse(
                status=200,
                message="Vehicles retrieved",
                data={
                    "vehicles": [VehicleResponse.model_validate(vehicle) for vehicle in result["items"]],
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def create_vehicle(self, data: dict) -> ApiResponse[VehicleResponse]:
        async with self.uow as uow:
            data["created_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
            vehicle = await uow.vehicle_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Vehicle created", data=VehicleResponse.model_validate(vehicle))

    async def update_vehicle(self, vehicle_id: int, data: dict) -> ApiResponse[VehicleResponse]:
        async with self.uow as uow:
            vehicle = await uow.vehicle_repository.get_by(id=vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")
            updated_vehicle = await uow.vehicle_repository.update(vehicle, data)
            await uow.commit()
            return ApiResponse(status=200, message="Vehicle updated",
                               data=VehicleResponse.model_validate(updated_vehicle))

    async def delete_vehicle(self, vehicle_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            vehicle = await uow.vehicle_repository.get_by(id=vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")
            await uow.vehicle_repository.soft_delete(vehicle)
            await uow.commit()
            return ApiResponse(status=200, message="Vehicle deleted", data=None)
