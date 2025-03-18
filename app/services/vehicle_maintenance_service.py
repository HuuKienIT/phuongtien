from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import ApiResponse
from ..unit_of_work import UnitOfWork
from ..schemas import VehicleMaintenanceResponse

class VehicleMaintenanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.uow = UnitOfWork(db)

    async def get_maintenance_by_id(self, maintenance_id: int) -> ApiResponse[VehicleMaintenanceResponse]:
        async with self.uow as uow:
            maintenance = await uow.vehicle_maintenance_repository.get_by(maintenance_id=maintenance_id)
            if not maintenance:
                raise HTTPException(status_code=404, detail="Maintenance not found")
            return ApiResponse(status=200, message="Maintenance found",
                               data=VehicleMaintenanceResponse.model_validate(maintenance))

    async def get_all_maintenances(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.vehicle_maintenance_repository.get_all(page, page_size)
            return ApiResponse(
                status=200,
                message="Maintenances retrieved",
                data={
                    "maintenances": [VehicleMaintenanceResponse.model_validate(maintenance) for maintenance in result["items"]],
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def create_maintenance(self, data: dict) -> ApiResponse[VehicleMaintenanceResponse]:
        async with self.uow as uow:
            maintenance = await uow.vehicle_maintenance_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Maintenance created",
                               data=VehicleMaintenanceResponse.model_validate(maintenance))

    async def update_maintenance(self, maintenance_id: int, data: dict) -> ApiResponse[VehicleMaintenanceResponse]:
        async with self.uow as uow:
            maintenance = await uow.vehicle_maintenance_repository.get_by(maintenance_id=maintenance_id)
            if not maintenance:
                raise HTTPException(status_code=404, detail="Maintenance not found")
            updated_maintenance = await uow.vehicle_maintenance_repository.update(maintenance, data)
            await uow.commit()
            return ApiResponse(status=200, message="Maintenance updated",
                               data=VehicleMaintenanceResponse.model_validate(updated_maintenance))

    async def delete_maintenance(self, maintenance_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            maintenance = await uow.vehicle_maintenance_repository.get_by(maintenance_id=maintenance_id)
            if not maintenance:
                raise HTTPException(status_code=404, detail="Maintenance not found")
            await uow.vehicle_maintenance_repository.soft_delete(maintenance)
            await uow.commit()
            return ApiResponse(status=200, message="Maintenance deleted", data=None)
