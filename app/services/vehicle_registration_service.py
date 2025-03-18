from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils import ApiResponse
from ..unit_of_work import UnitOfWork
from ..schemas import VehicleRegistrationResponse

class VehicleRegistrationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.uow = UnitOfWork(db)

    async def get_registration_by_id(self, registration_id: int) -> ApiResponse[VehicleRegistrationResponse]:
        async with self.uow as uow:
            registration = await uow.vehicle_registration_repository.get_by(filters={"id": registration_id})
            if not registration:
                raise HTTPException(status_code=404, detail="Vehicle registration not found")
            return ApiResponse(status=200, message="Registration found", data=VehicleRegistrationResponse.model_validate(registration))

    async def get_all_registrations(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.vehicle_registration_repository.get_all(page=page, page_size=page_size)
            return ApiResponse(
                status=200,
                message="Vehicle registrations retrieved",
                data={
                    "registrations": self._convert_to_response(result["items"]),
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def get_registrations_by_vehicle_id(self, vehicle_id: int) -> ApiResponse[list[VehicleRegistrationResponse]]:
        async with self.uow as uow:
            result = await uow.vehicle_registration_repository.get_all(filters={"vehicle_id": vehicle_id})
            return ApiResponse(
                status=200,
                message="Vehicle registrations retrieved",
                data=self._convert_to_response(result["items"])
            )

    async def create_registration(self, data: dict) -> ApiResponse[VehicleRegistrationResponse]:
        async with self.uow as uow:
            data["created_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
            registration = await uow.vehicle_registration_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Vehicle registration created", data=VehicleRegistrationResponse.model_validate(registration))

    async def update_registration(self, registration_id: int, data: dict) -> ApiResponse[VehicleRegistrationResponse]:
        async with self.uow as uow:
            registration = await uow.vehicle_registration_repository.get_by(filters={"id": registration_id})
            if not registration:
                raise HTTPException(status_code=404, detail="Vehicle registration not found")
            updated_registration = await uow.vehicle_registration_repository.update(registration, data)
            await uow.commit()
            return ApiResponse(status=200, message="Vehicle registration updated", data=VehicleRegistrationResponse.model_validate(updated_registration))

    async def delete_registration(self, registration_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            registration = await uow.vehicle_registration_repository.get_by(filters={"id": registration_id})
            if not registration:
                raise HTTPException(status_code=404, detail="Vehicle registration not found")
            await uow.vehicle_registration_repository.soft_delete(registration)
            await uow.commit()
            return ApiResponse(status=200, message="Vehicle registration deleted", data=None)

    def _convert_to_response(self, items: list) -> list[VehicleRegistrationResponse]:
        """Chuyển đổi danh sách đăng ký thành danh sách `VehicleRegistrationResponse`"""
        return [VehicleRegistrationResponse.model_validate(registration) for registration in items]
