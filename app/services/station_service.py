from datetime import datetime, timezone
from ..schemas import StationResponse
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
            station = await uow.station_repository.get_by(id=station_id)
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            return ApiResponse(status=200, message="Station found", data=StationResponse.model_validate(station))

    async def get_all_stations(self, page: int, page_size: int) -> ApiResponse[dict]:
        async with self.uow as uow:
            result = await uow.station_repository.get_all(page, page_size)
            return ApiResponse(
                status=200,
                message="Stations retrieved",
                data={
                    "stations": [StationResponse.model_validate(station) for station in result["items"]],
                    "total_items": result.get("total_items"),
                    "current_page": result.get("current_page"),
                    "page_size": result.get("page_size")
                }
            )

    async def create_station(self, data: dict) -> ApiResponse[StationResponse]:
        async with self.uow as uow:
            data["created_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
            station = await uow.station_repository.create(data)
            await uow.commit()
            return ApiResponse(status=201, message="Station created", data=StationResponse.model_validate(station))

    async def update_station(self, station_id: int, data: dict) -> ApiResponse[StationResponse]:
        async with self.uow as uow:
            station = await uow.station_repository.get_by(id=station_id)
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            data["updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
            updated_station = await uow.station_repository.update(station, data)
            await uow.commit()
            return ApiResponse(status=200, message="Station updated", data=StationResponse.model_validate(updated_station))

    async def soft_delete_station(self, station_id: int) -> ApiResponse[None]:
        async with self.uow as uow:
            station = await uow.station_repository.get_by(id=station_id)
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            await uow.station_repository.soft_delete(station)
            await uow.commit()
            return ApiResponse(status=200, message="Station soft-deleted", data=None)
