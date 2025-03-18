from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Vehicle
from .base_repository import BaseRepository

class VehicleRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Vehicle)