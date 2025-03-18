from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    total_slots = Column(Integer, nullable=False)
    total_vehicles = Column(Integer, nullable=False)
    available_vehicles = Column(Integer, nullable=False)
    charging_capacity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, server_default='operational')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    station_vehicles = relationship("StationVehicle", back_populates="station")
    vehicle_battery_logs = relationship("VehicleBatteryLog", back_populates="station")


class StationVehicle(Base):
    __tablename__ = 'station_vehicles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    arrival_time = Column(DateTime(timezone=True), server_default=func.now())
    departure_time = Column(DateTime(timezone=True), nullable=True)
    charging_status = Column(String, nullable=False, server_default='charging')

    station = relationship("Station", back_populates="station_vehicles")
    vehicle = relationship("Vehicle", back_populates="station_vehicles")


class VehicleModel(Base):
    __tablename__ = 'vehicle_models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String, nullable=False, unique=True)
    manufacture_year = Column(Integer, nullable=False)
    origin = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=False)
    engine_power = Column(Float, nullable=False)
    battery_type = Column(String, nullable=False)
    battery_capacity = Column(Float, nullable=False)
    nominal_battery_voltage = Column(Float, nullable=True)
    range_per_charge = Column(Float, nullable=True)
    vehicle_weight = Column(Float, nullable=True)
    max_load = Column(Float, nullable=True)
    braking_system = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vehicles = relationship("Vehicle", back_populates="vehicle_model")


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    licence_plate = Column(String, nullable=False, unique=True)
    vehicle_model_id = Column(Integer, ForeignKey('vehicle_models.id'), nullable=False)
    color = Column(String, nullable=True)
    current_battery_capacity = Column(Float, nullable=False)
    current_station_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    total_km_driven = Column(Float, nullable=False, default=0.0)
    last_maintenance_date = Column(DateTime(timezone=True), nullable=True)
    next_maintenance_due = Column(DateTime(timezone=True), nullable=True)
    insurance_expiry_date = Column(DateTime(timezone=True), nullable=True)
    qr_code = Column(String, nullable=True)
    status = Column(String, nullable=False, server_default='available')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    vehicle_model = relationship("VehicleModel", back_populates="vehicles")
    station_vehicles = relationship("StationVehicle", back_populates="vehicle")
    vehicle_insurance = relationship("VehicleInsurance", back_populates="vehicle", uselist=False)
    vehicle_tracking = relationship("VehicleTracking", back_populates="vehicle")
    vehicle_maintenance = relationship("VehicleMaintenance", back_populates="vehicle")
    vehicle_battery_logs = relationship("VehicleBatteryLog", back_populates="vehicle")
    vehicle_registrations = relationship("VehicleRegistration", back_populates="vehicle")


class VehicleInsurance(Base):
    __tablename__ = 'vehicle_insurances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    provider_name = Column(String, nullable=False)
    policy_number = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    expiry_date = Column(DateTime(timezone=True), nullable=False)
    coverage_details = Column(Text, nullable=True)
    status = Column(String, nullable=False, server_default='active')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vehicle = relationship("Vehicle", back_populates="vehicle_insurance")


class VehicleMaintenance(Base):
    __tablename__ = 'vehicle_maintenances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    maintenance_type = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    cost = Column(Float, nullable=False)
    maintenance_details = Column(Text, nullable=True)
    status = Column(String, nullable=False,
                    server_default='scheduled')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vehicle = relationship("Vehicle", back_populates="vehicle_maintenance")


class VehicleRegistration(Base):
    __tablename__ = 'vehicle_registrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    registration_number = Column(String, nullable=False, unique=True)
    agency = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, server_default='pending')
    note = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vehicle = relationship("Vehicle", back_populates="vehicle_registrations")


class VehicleTracking(Base):
    __tablename__ = 'vehicle_tracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    current_latitude = Column(Float, nullable=False)
    current_longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    battery_level = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vehicle = relationship("Vehicle", back_populates="vehicle_tracking")


class VehicleBatteryLog(Base):
    __tablename__ = 'vehicle_battery_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    battery_before = Column(Float, nullable=False)
    battery_after = Column(Float, nullable=False)
    energy_used = Column(Float, nullable=False)

    vehicle = relationship("Vehicle", back_populates="vehicle_battery_logs")
    station = relationship("Station", back_populates="vehicle_battery_logs")
