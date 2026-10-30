from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Appointment, Doctor, Patient
from app.schemas.appointment import AppointmentCreate


def book_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    doctor = db.get(Doctor, data.doctor_id)
    patient = db.get(Patient, data.patient_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    requested_end = data.starts_at + timedelta(minutes=data.duration_minutes)
    existing = db.scalars(
        select(Appointment).where(
            Appointment.doctor_id == data.doctor_id,
            Appointment.status == "booked",
        )
    ).all()
    for appointment in existing:
        existing_end = appointment.starts_at + timedelta(minutes=appointment.duration_minutes)
        if data.starts_at < existing_end and appointment.starts_at < requested_end:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Doctor already has an appointment during this time",
            )

    appointment = Appointment(**data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def cancel_appointment(db: Session, appointment_id: int) -> Appointment:
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appointment.status == "cancelled":
        raise HTTPException(status_code=409, detail="Appointment is already cancelled")
    appointment.status = "cancelled"
    db.commit()
    db.refresh(appointment)
    return appointment
