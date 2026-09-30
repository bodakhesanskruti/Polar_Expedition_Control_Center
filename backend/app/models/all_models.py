from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from ..database.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(40), default="OPERATOR", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Expedition(Base):
    __tablename__ = "expeditions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    code: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)
    destination: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="PLANNED", nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    expedition_id: Mapped[int | None] = mapped_column(ForeignKey("expeditions.id"), nullable=True)


class Personnel(Base):
    __tablename__ = "personnel"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="ACTIVE", nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)


class Cargo(Base):
    __tablename__ = "cargo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    tracking_code: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(180), nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PLANNED", nullable=False)
    priority: Mapped[str] = mapped_column(String(30), default="NORMAL", nullable=False)


class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    location_type: Mapped[str] = mapped_column(String(50), default="WAYPOINT", nullable=False)


class CargoTracking(Base):
    __tablename__ = "cargo_tracking"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cargo_id: Mapped[int] = mapped_column(ForeignKey("cargo.id"), nullable=False)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    transport_mode: Mapped[str] = mapped_column(String(40), default="VEHICLE", nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (Index("ix_cargo_tracking_cargo_time", "cargo_id", "recorded_at"),)


class PersonnelLocation(Base):
    __tablename__ = "personnel_locations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    personnel_id: Mapped[int] = mapped_column(ForeignKey("personnel.id"), nullable=False)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="MOVING", nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (Index("ix_personnel_location_person_time", "personnel_id", "recorded_at"),)


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), default="units", nullable=False)
    min_quantity: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="AVAILABLE", nullable=False)


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"), nullable=False)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Checkin(Base):
    __tablename__ = "checkins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    personnel_id: Mapped[int] = mapped_column(ForeignKey("personnel.id"), nullable=False)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    checkin_type: Mapped[str] = mapped_column(String(40), default="ROUTINE", nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmergencyIncident(Base):
    __tablename__ = "emergency_incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    personnel_id: Mapped[int | None] = mapped_column(ForeignKey("personnel.id"), nullable=True)
    incident_type: Mapped[str] = mapped_column(String(60), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="OPEN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expedition_id: Mapped[int] = mapped_column(ForeignKey("expeditions.id"), nullable=False)
    personnel_id: Mapped[int | None] = mapped_column(ForeignKey("personnel.id"), nullable=True)
    cargo_id: Mapped[int | None] = mapped_column(ForeignKey("cargo.id"), nullable=True)
    inventory_id: Mapped[int | None] = mapped_column(ForeignKey("inventory.id"), nullable=True)
    incident_id: Mapped[int | None] = mapped_column(ForeignKey("emergency_incidents.id"), nullable=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), default="MEDIUM", nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="OPEN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class EmergencyResponse(Base):
    __tablename__ = "emergency_responses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("emergency_incidents.id"), nullable=False)
    responder: Mapped[str] = mapped_column(String(120), nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="ASSIGNED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
