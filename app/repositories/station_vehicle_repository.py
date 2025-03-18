from sqlalchemy.ext.asyncio import AsyncSession
from ..models import StationVehicle
from .base_repository import BaseRepository

class StationVehicleRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, StationVehicle)