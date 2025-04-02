from models.models import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, Path
from fastapi.responses import JSONResponse
from models.database import get_db
from typing import Annotated

router = APIRouter(prefix="/api/dentists", tags=["Dentists"])

@router.get("/")
def get_people(db: Session = Depends(get_db)):
    return db.query(Dentist).all()

@router.get("/")
def get_dentist(id: Annotated[int, Path(..., ge=1)], db: Session = Depends(get_db)):

    person = db.query(Dentist).filter(Dentist.id == id).first()

    if person==None:
        return JSONResponse(status_code=404, content={ "message": "Користувач не знайдений"})

    return person


@router.post("/")
def create_dentist(data = Body(), db: Session = Depends(get_db)):
    dentist = Dentist(name=data["name"], age=data["age"], experience=data["experience"], phoneNumber=data["phoneNumber"])
    db.add(dentist)
    db.commit()
    db.refresh(dentist)
    return dentist


@router.put("/")
def edit_dentist(data = Body(), db: Session = Depends(get_db)):
    dentist = db.query(Dentist).filter(Dentist.id == data["id"]).first()

    if dentist == None:
        return JSONResponse(status_code=404, content={ "message": "Користувач не знайдений"})

    dentist.age = data["age"]
    dentist.name = data["name"]
    db.commit()
    db.refresh(dentist)
    return dentist


@router.delete("/")
def delete_dentist(id, db: Session = Depends(get_db)):

    dentist = db.query(Dentist).filter(Dentist.id == id).first()

    if dentist == None:
       return JSONResponse( status_code=404, content={ "message": "Користувач не знайдений"})

    db.delete(dentist)
    db.commit()
    return dentist