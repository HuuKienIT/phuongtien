from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import StationRequest
from ..services import StationService
from ..data import get_db

station_router = APIRouter(prefix="/stations", tags=["Stations"])

@station_router.get("/{station_id}")
async def get_station_by_id(station_id: int, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.get_station_by_id(station_id)

@station_router.get("/search/")
async def search_stations(name: str, page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.search_stations_by_name(name, page, page_size)

@station_router.get("/{station_id}/vehicles")
async def get_station_with_vehicles(station_id: int, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.get_station_with_vehicles(station_id)

@station_router.get("/")
async def get_all_stations(page: Optional[int] = None, page_size: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.get_all_stations(page, page_size)

@station_router.post("/")
async def create_station(data: StationRequest, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.create_station(data.model_dump())

@station_router.put("/{station_id}")
async def update_station(station_id: int, data: StationRequest, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.update_station(station_id, data.model_dump())

@station_router.delete("/{station_id}/soft")
async def soft_delete_station(station_id: int, db: AsyncSession = Depends(get_db)):
    station_service = StationService(db)
    return await station_service.soft_delete_station(station_id)
