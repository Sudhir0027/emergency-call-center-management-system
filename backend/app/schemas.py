from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class Role(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"

class EmergencyType(str, Enum):
    MEDICAL = "Medical Emergency"
    FIRE = "Fire"
    POLICE = "Police"
    ACCIDENT = "Road Accident"
    DISASTER = "Natural Disaster"
    MISSING = "Missing Person"
    RESCUE = "Rescue"
    OTHER = "Other"

class CallStatus(str, Enum):
    WAITING = "WAITING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"

class ResponderType(str, Enum):
    AMBULANCE = "AMBULANCE"
    FIRE = "FIRE"
    POLICE = "POLICE"
    RESCUE = "RESCUE"

class Availability(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: Role = Role.OPERATOR

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: Role
    created_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CallCreate(BaseModel):
    caller_name: str = Field(min_length=2, max_length=100)
    caller_phone: str = Field(min_length=7, max_length=20)
    location: str = Field(min_length=2, max_length=200)
    emergency_type: EmergencyType
    description: str = Field(min_length=3, max_length=2000)
    priority: int = Field(ge=1, le=5)

    @field_validator("caller_phone")
    @classmethod
    def phone(cls, v):
        cleaned = v.replace("+", "").replace("-", "").replace(" ", "")
        if not cleaned.isdigit():
            raise ValueError("Phone number must contain digits, spaces, + or - only")
        return v

class CallUpdate(BaseModel):
    caller_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    caller_phone: Optional[str] = Field(default=None, min_length=7, max_length=20)
    location: Optional[str] = Field(default=None, min_length=2, max_length=200)
    emergency_type: Optional[EmergencyType] = None
    description: Optional[str] = Field(default=None, min_length=3, max_length=2000)

class PriorityUpdate(BaseModel):
    priority: int = Field(ge=1, le=5)

class StatusUpdate(BaseModel):
    status: CallStatus

class ResponderCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    type: ResponderType
    phone: str = Field(min_length=7, max_length=20)
    vehicle_number: str = Field(min_length=2, max_length=40)
    location: str = Field(min_length=2, max_length=200)
    availability: Availability = Availability.AVAILABLE

class ResponderUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    type: Optional[ResponderType] = None
    phone: Optional[str] = Field(default=None, min_length=7, max_length=20)
    vehicle_number: Optional[str] = Field(default=None, min_length=2, max_length=40)
    location: Optional[str] = Field(default=None, min_length=2, max_length=200)
    availability: Optional[Availability] = None

class ResponderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    responder_id: int
    name: str
    type: ResponderType
    phone: str
    vehicle_number: str
    location: str
    availability: Availability
    created_at: datetime

class CallOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    call_id: int
    caller_name: str
    caller_phone: str
    location: str
    emergency_type: EmergencyType
    description: str
    priority: int
    status: CallStatus
    created_at: datetime
    assigned_responder_id: Optional[int]
    updated_at: datetime
    responder: Optional[ResponderOut] = None
