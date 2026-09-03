import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, default="Inspector Operator-1")
    role = Column(String(50), nullable=False, default="procurement_agent")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    inspections = relationship("Inspection", back_populates="user")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inspection_id = Column(String(36), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    grain_type = Column(String(50), nullable=False, default="rice")
    farmer_reference = Column(String(100), nullable=True)
    image_path = Column(String(255), nullable=True)
    annotated_image_path = Column(String(255), nullable=True)
    total_objects = Column(Integer, default=0)
    quality_score = Column(Float, default=0.0)
    status = Column(String(30), nullable=False, default="PENDING")
    ai_mode = Column(String(20), nullable=False, default="demo")
    processing_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="inspections")
    detections = relationship("Detection", back_populates="inspection", cascade="all, delete-orphan")
    quality_result = relationship("QualityResult", back_populates="inspection", uselist=False, cascade="all, delete-orphan")
    certificate = relationship("Certificate", back_populates="inspection", uselist=False, cascade="all, delete-orphan")


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    class_name = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    x1 = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    area = Column(Float, nullable=False)

    inspection = relationship("Inspection", back_populates="detections")


class QualityResult(Base):
    __tablename__ = "quality_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), unique=True, nullable=False)
    whole_percentage = Column(Float, nullable=False, default=0.0)
    broken_percentage = Column(Float, nullable=False, default=0.0)
    discolored_percentage = Column(Float, nullable=False, default=0.0)
    insect_damage_percentage = Column(Float, nullable=False, default=0.0)
    foreign_matter_percentage = Column(Float, nullable=False, default=0.0)
    quality_score = Column(Float, nullable=False, default=0.0)
    category = Column(String(50), nullable=False, default="Needs Review")
    decision = Column(String(50), nullable=False, default="CONDITIONAL")
    penalty_details = Column(Text, nullable=True)

    inspection = relationship("Inspection", back_populates="quality_result")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), unique=True, nullable=False)
    certificate_number = Column(String(64), unique=True, index=True, nullable=False)
    verification_token = Column(String(64), unique=True, index=True, nullable=False)
    qr_code_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    inspection = relationship("Inspection", back_populates="certificate")
