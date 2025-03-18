from datetime import datetime, timezone
from typing import Optional

from ..schemas import StationResponse, VehicleResponse
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import ApiResponse
from ..unit_of_work import UnitOfWork

class StationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.uow = UnitOfWork(db)

    async def get_station_by_id(self, station_id: int) -> ApiResponse[StationResponse]:
        async with self.uow as uow:
            station = await uow.station_repository.get_by(filters={"id": station_id})
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            return ApiResponse(status=200, message="Station found", data=StationResponse.model_validate(station))

    async def search_stations_by_name(self, name: str, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.station_repository.get_all(
                like_filters={"name": f"%{name}%"},
                page=page,
                page_size=page_size
            )
            return ApiResponse(
                status=200,
                message="Stations found",
                data={
                    "stations": [StationResponse.model_validate(station) for station in result["items"]],
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def get_station_with_vehicles(self, station_id: int) -> ApiResponse[dict]:
        """Lấy thông tin trạm và danh sách xe trong trạm"""
        async with self.uow as uow:
            station = await uow.station_repository.get_by(
                filters={"id": station_id},
                relationships=["station_vehicles", "station_vehicles.vehicle"]
            )
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")

            return ApiResponse(
                status=200,
                message="Station and vehicles retrieved",
                data={
                    "station": StationResponse.model_validate(station),
                    "vehicles": [VehicleResponse.model_validate(sv.vehicle) for sv in station.station_vehicles]
                }
            )

    async def get_all_stations(self, page: Optional[int] = None, page_size: Optional[int] = None) -> ApiResponse[dict]:
        """Lấy danh sách trạm, hỗ trợ cả phân trang và không phân trang."""
        async with self.uow as uow:
            result = await uow.station_repository.get_all(page=page, page_size=page_size)

            stations = [StationResponse.model_validate(station) for station in result["items"]]

            if page and page_size:
                return ApiResponse(
                    status=200,
                    message="Stations retrieved with pagination",
                    data={
                        "stations": stations,
                        "total_items": result.get("total_items"),
                        "current_page": page,
                        "page_size": page_size
                    }
                )

            return ApiResponse(status=200, message="All stations retrieved", data=stations)

    async def create_station(self, data: dict) -> ApiResponse[StationResponse]:
        async with self.uow as uow:
            data["created_at"] = datetime.now(timezone.utc)
            station = await uow.station_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Station created", data=StationResponse.model_validate(station))

    async def update_station(self, station_id: int, data: dict) -> ApiResponse[StationResponse]:
        async with self.uow as uow:
            station = await uow.station_repository.get_by(filters={"id": station_id})
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            data["updated_at"] = datetime.now(timezone.utc)
            updated_station = await uow.station_repository.update(station, data)
            await uow.commit()
            return ApiResponse(status=200, message="Station updated", data=StationResponse.model_validate(updated_station))

    async def soft_delete_station(self, station_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            station = await uow.station_repository.get_by(filters={"id": station_id})
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            await uow.station_repository.soft_delete(station)
            await uow.commit()
            return ApiResponse(status=200, message="Station soft-deleted", data=None)
