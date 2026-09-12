from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="OPERATOR")
    created_at = Column(DateTime(timezone=True), default=utcnow)

class Responder(Base):
    __tablename__ = "responders"
    responder_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(30), nullable=False)
    phone = Column(String(20), nullable=False)
    vehicle_number = Column(String(40), nullable=False)
    location = Column(String(200), nullable=False)
    availability = Column(String(20), nullable=False, default="AVAILABLE")
    created_at = Column(DateTime(timezone=True), default=utcnow)
    calls = relationship("EmergencyCall", back_populates="responder")

class EmergencyCall(Base):
    __tablename__ = "emergency_calls"
    call_id = Column(Integer, primary_key=True, index=True)
    caller_name = Column(String(100), nullable=False)
    caller_phone = Column(String(20), nullable=False)
    location = Column(String(200), nullable=False)
    emergency_type = Column(String(40), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Integer, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="WAITING", index=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, index=True)
    assigned_responder_id = Column(Integer, ForeignKey("responders.responder_id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    responder = relationship("Responder", back_populates="calls")
    history = relationship("CallHistory", back_populates="call", cascade="all, delete-orphan")

class CallHistory(Base):
    __tablename__ = "call_history"
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey("emergency_calls.call_id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String(20), nullable=True)
    new_status = Column(String(20), nullable=False)
    changed_by = Column(String(80), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=utcnow)
    call = relationship("EmergencyCall", back_populates="history")
