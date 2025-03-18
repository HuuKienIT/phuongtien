from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Vehicle
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
            return ApiResponse(status=200, message="Vehicle found", data=self._convert_to_response(vehicle))

    async def get_all_vehicles(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.vehicle_repository.get_all(page=page, page_size=page_size)
            return ApiResponse(
                status=200,
                message="Vehicles retrieved",
                data={
                    "vehicles": self._convert_to_response(result["items"]),
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def get_unassigned_vehicles(self) -> ApiResponse[list[VehicleResponse]]:
        async with self.uow as uow:
            result = await uow.vehicle_repository.get_all(filters={"current_station_id": None})
            return ApiResponse(
                status=200,
                message="Unassigned vehicles retrieved",
                data=self._convert_to_response(result["items"])
            )

    async def search_vehicles_by_licence_plate(self, licence_plate: str, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.vehicle_repository.get_all(
                like_filters={"licence_plate": f"%{licence_plate}%"},
                page=page,
                page_size=page_size
            )
            return ApiResponse(
                status=200,
                message="vehicles found",
                data={
                    "vehicles": self._convert_to_response(result["items"]),
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def create_vehicle(self, data: dict) -> ApiResponse[VehicleResponse]:
        async with self.uow as uow:
            # Kiểm tra xe đã tồn tại chưa
            exists = await uow.vehicle_repository.get_by(filters={"license_plate": data.get("license_plate")})
            if exists:
                raise HTTPException(status_code=400, detail="Vehicle already exists")

            data.setdefault("created_at", datetime.now(timezone.utc).replace(tzinfo=None))
            vehicle = await uow.vehicle_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Vehicle created", data=self._convert_to_response(vehicle))

    async def update_vehicle(self, vehicle_id: int, data: dict) -> ApiResponse[VehicleResponse]:
        async with self.uow as uow:
            vehicle = await uow.vehicle_repository.get_by(id=vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")

            data.setdefault("updated_at", datetime.now(timezone.utc).replace(tzinfo=None))
            updated_vehicle = await uow.vehicle_repository.update(vehicle, data)
            await uow.commit()
            return ApiResponse(status=200, message="Vehicle updated", data=self._convert_to_response(updated_vehicle))

    async def delete_vehicle(self, vehicle_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            vehicle = await uow.vehicle_repository.get_by(id=vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")

            await uow.vehicle_repository.soft_delete(vehicle, {"updated_at": datetime.now(timezone.utc).replace(tzinfo=None)})
            await uow.commit()
            return ApiResponse(status=200, message="Vehicle deleted", data=None)

    def _convert_to_response(self, items) -> list[VehicleResponse] | VehicleResponse:
        """Chuyển đổi đối tượng Vehicle hoặc danh sách thành `VehicleResponse`"""
        if isinstance(items, list):
            return [VehicleResponse.model_validate(vehicle) for vehicle in items]
        return VehicleResponse.model_validate(items)
