from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Station
from .base_repository import BaseRepository

class StationRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Station)
