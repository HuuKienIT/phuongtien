from sqlalchemy.ext.asyncio import AsyncSession
from ..models import VehicleMaintenance
from .base_repository import BaseRepository

class VehicleMaintenanceRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, VehicleMaintenance)