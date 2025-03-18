from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from .data import init_db, get_db, seed_data
from .routes import (station_router, station_vehicle_router, vehicle_router,
                     vehicle_insurance_router, vehicle_maintenance_router, vehicle_registration_router)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Event handler chạy khi ứng dụng khởi động."""
    await init_db()  # Chạy migrations
    async for db in get_db():
        await seed_data(db)  # Seed dữ liệu
    print("✅ Dữ liệu đã được seed thành công.")
    yield

app = FastAPI(
    title="Vehicle Management API",
    version="1.0",
    description="API quản lý trạm xe và xe với FastAPI",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(station_router)
app.include_router(station_vehicle_router)
app.include_router(vehicle_router)
app.include_router(vehicle_insurance_router)
app.include_router(vehicle_maintenance_router)
app.include_router(vehicle_registration_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("Services.Vehicle.main:app", host="0.0.0.0", port=5000, reload=True)

