from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)
    starts_at: datetime
    duration_minutes: int = Field(default=30, ge=10, le=240)
    reason: str = Field(min_length=2, max_length=500)


class AppointmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor_id: int
    patient_id: int
    starts_at: datetime
    duration_minutes: int
    reason: str
    status: str
