from models.models import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from models.database import get_db

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.get("/")
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()


@router.get("/{id}")
def get_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Пацієнт не знайдений"})
    return patient


@router.post("/")
def create_patient(data=Body(), db: Session = Depends(get_db)):
    patient = Patient(
        name=data["name"],
        age=data["age"],
        phoneNumber=data["phoneNumber"],
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.put("/")
def update_patient(data=Body(), db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == data["id"]).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Пацієнт не знайдений"})

    patient.name = data["name"]
    patient.age = data["age"]
    patient.phoneNumber = data["phone"]

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{id}")
def delete_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Пацієнт не знайдений"})

    db.delete(patient)
    db.commit()
    return patient