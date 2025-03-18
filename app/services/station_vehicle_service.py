from datetime import datetime, timezone
from typing import List

from ..schemas import StationVehicleResponse
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import ApiResponse
from ..unit_of_work import UnitOfWork

class StationVehicleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.uow = UnitOfWork(db)

    async def get_station_vehicle_by_id(self, record_id: int) -> ApiResponse[StationVehicleResponse]:
        async with self.uow as uow:
            station_vehicle = await uow.station_vehicle_repository.get_by(filters={"id": record_id})
            if not station_vehicle:
                raise HTTPException(status_code=404, detail="Station vehicle record not found")
            return ApiResponse(status=200, message="Record found", data=StationVehicleResponse.model_validate(station_vehicle))

    async def get_all_station_vehicles(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.station_vehicle_repository.get_all(page=page, page_size=page_size)
            return ApiResponse(
                status=200,
                message="Station vehicle retrieved",
                data={
                    "station_vehicle": [StationVehicleResponse.model_validate(sv) for sv in result["items"]],
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def create_station_vehicle(self, data: dict) -> ApiResponse[StationVehicleResponse]:
        async with self.uow as uow:
            data["arrival_time"] = datetime.now(timezone.utc)
            station_vehicle = await uow.station_vehicle_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Station vehicle record created", data=StationVehicleResponse.model_validate(station_vehicle))

    async def create_bulk_station_vehicles(self, data: dict) -> ApiResponse[List[StationVehicleResponse]]:
        async with self.uow as uow:
            station_id = data["station_id"]
            vehicles = data["vehicles"]
            created_vehicles = [
                StationVehicleResponse.model_validate(await uow.station_vehicle_repository.create({
                    **vehicle, "station_id": station_id, "arrival_time": datetime.now(timezone.utc)
                }))
                for vehicle in vehicles
            ]
            await uow.commit()
            return ApiResponse(status=201, message="Multiple station vehicles added", data=created_vehicles)

    async def update_station_vehicle(self, record_id: int, data: dict) -> ApiResponse[StationVehicleResponse]:
        async with self.uow as uow:
            station_vehicle = await uow.station_vehicle_repository.get_by(filters={"id": record_id})
            if not station_vehicle:
                raise HTTPException(status_code=404, detail="Station vehicle record not found")
            updated_station_vehicle = await uow.station_vehicle_repository.update(station_vehicle, data)
            await uow.commit()
            return ApiResponse(status=200, message="Record updated", data=StationVehicleResponse.model_validate(updated_station_vehicle))

    async def delete_station_vehicle(self, record_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            station_vehicle = await uow.station_vehicle_repository.get_by(filters={"id": record_id})
            if not station_vehicle:
                raise HTTPException(status_code=404, detail="Station vehicle record not found")
            await uow.station_vehicle_repository.soft_delete(station_vehicle)
            await uow.commit()
            return ApiResponse(status=200, message="Record deleted", data=None)
