from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import (StationRepository, StationVehicleRepository, VehicleRepository,
                            VehicleInsuranceRepository, VehicleMaintenanceRepository)

class UnitOfWork:
    def __init__(self, db: AsyncSession):
        if not isinstance(db, AsyncSession):
            raise ValueError("Database session must be an instance of AsyncSession")
        self.db = db
        self.station_repository = StationRepository(db)
        self.station_vehicle_repository = StationVehicleRepository(db)
        self.vehicle_repository = VehicleRepository(db)
        self.vehicle_insurance_repository = VehicleInsuranceRepository(db)
        self.vehicle_maintenance_repository = VehicleMaintenanceRepository(db)

    async def rollback(self):
        if self.db:
            await self.db.rollback()

    async def commit(self):
        if self.db:
            await self.db.commit()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.db.close()
