from models.models import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from models.database import get_db

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@router.get("/{id}")
def get_appointment(id: int, db: Session = Depends(get_db)):
    patient = db.query(Appointment).filter(Appointment.id == id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Запис не знайдено"})
    return patient


@router.post("/")
def create_appointment(data=Body(), db: Session = Depends(get_db)):
    appointment = Appointment(
        name=data["name"],
        age=data["age"],
        phoneNumber=data["phoneNumber"],
        reason = data["reason"]
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.put("/")
def update_appointment(data=Body(), db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == data["id"]).first()
    if not appointment:
        return JSONResponse(status_code=404, content={"message": "Запис не знайдено"})

    appointment.name = data["name"]
    appointment.age = data["age"]
    appointment.phoneNumber = data["phone"]

    db.commit()
    db.refresh(appointment)
    return appointment


@router.delete("/{id}")
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        return JSONResponse(status_code=404, content={"message": "Запис не знайдено"})

    db.delete(appointment)
    db.commit()
    return appointment