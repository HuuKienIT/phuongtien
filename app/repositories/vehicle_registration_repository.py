from sqlalchemy.ext.asyncio import AsyncSession
from ..models import VehicleRegistration
from .base_repository import BaseRepository

class VehicleRegistrationRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, VehicleRegistration)