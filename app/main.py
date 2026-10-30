from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.models import Appointment, Doctor, Patient  # noqa: F401 - register model metadata
from app.routers import appointments, doctors, patients


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Hospital Appointment Booking API",
    description="A learning project for booking appointments with hospital doctors.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
