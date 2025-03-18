from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)
    total_slots = Column(Integer, nullable=False)
    available_vehicles = Column(Integer, nullable=False)
    charging_capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    status = Column(String, nullable=False)

    station_vehicles = relationship("StationVehicle", back_populates="station")
    vehicle_battery_logs = relationship("VehicleBatteryLog", back_populates="station")

class StationVehicle(Base):
    __tablename__ = 'station_vehicles'

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    arrival_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    departure_time = Column(DateTime(timezone=True), nullable=True)
    charging_status = Column(String, nullable=False)

    station = relationship("Station", back_populates="station_vehicles")
    vehicle = relationship("Vehicle", back_populates="station_vehicles")

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    licence_plate = Column(String, nullable=False, unique=True)
    model = Column(String, nullable=False)
    battery_capacity = Column(Integer, nullable=False)
    current_station_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    total_km_driven = Column(Integer, nullable=False, default=0)
    last_maintenance_date = Column(DateTime(timezone=True), nullable=True)
    next_maintenance_due = Column(DateTime(timezone=True), nullable=True)
    insurance_expiry_date = Column(DateTime(timezone=True), nullable=True)
    qr_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    station_vehicles = relationship("StationVehicle", back_populates="vehicle")
    vehicle_insurance = relationship("VehicleInsurance", back_populates="vehicle", uselist=False)
    vehicle_tracking = relationship("VehicleTracking", back_populates="vehicle")
    vehicle_maintenance = relationship("VehicleMaintenance", back_populates="vehicle")
    vehicle_battery_logs = relationship("VehicleBatteryLog", back_populates="vehicle")

class VehicleInsurance(Base):
    __tablename__ = 'vehicle_insurances'

    insurance_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    provider_name = Column(String, nullable=False)
    policy_number = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    expiry_date = Column(DateTime(timezone=True), nullable=False)
    coverage_details = Column(String, nullable=True)

    vehicle = relationship("Vehicle", back_populates="vehicle_insurance")

class VehicleMaintenance(Base):
    __tablename__ = 'vehicle_maintenances'

    maintenance_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    maintenance_type = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime(timezone=True), nullable=True)
    cost = Column(Integer, nullable=False)
    maintenance_details = Column(String, nullable=True)

    vehicle = relationship("Vehicle", back_populates="vehicle_maintenance")

class VehicleTracking(Base):
    __tablename__ = 'vehicle_tracking'

    tracking_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    current_latitude = Column(Integer, nullable=False)
    current_longitude = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    battery_level = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    vehicle = relationship("Vehicle", back_populates="vehicle_tracking")

class VehicleBatteryLog(Base):
    __tablename__ = 'vehicle_battery_logs'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    start_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime(timezone=True), nullable=True)
    battery_before = Column(Integer, nullable=False)
    battery_after = Column(Integer, nullable=False)
    energy_used = Column(Integer, nullable=False)

    vehicle = relationship("Vehicle", back_populates="vehicle_battery_logs")
    station = relationship("Station", back_populates="vehicle_battery_logs")