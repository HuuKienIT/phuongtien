from sqlalchemy.ext.asyncio import AsyncSession
from ..models import VehicleInsurance
from .base_repository import BaseRepository

class VehicleInsuranceRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, VehicleInsurance)