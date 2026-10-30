from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentRead
from app.services.appointments import book_appointment, cancel_appointment

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    return book_appointment(db, data)


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    doctor_id: int | None = Query(default=None, gt=0),
    patient_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    query = select(Appointment).order_by(Appointment.starts_at)
    if doctor_id is not None:
        query = query.where(Appointment.doctor_id == doctor_id)
    if patient_id is not None:
        query = query.where(Appointment.patient_id == patient_id)
    return db.scalars(query).all()


@router.delete("/{appointment_id}", response_model=AppointmentRead)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    if appointment_id <= 0:
        raise HTTPException(status_code=400, detail="Appointment ID must be positive")
    return cancel_appointment(db, appointment_id)
