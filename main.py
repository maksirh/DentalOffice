from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

# визначаємо залежність
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return FileResponse("public/home.html")

@app.get("/api/dentists")
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()

@app.get("/api/dentists/{id}")
def get_person(id, db: Session = Depends(get_db)):

    # отримуємо користувача за id
    person = db.query(Person).filter(Person.id == id).first()

    if person==None:
        return JSONResponse(status_code=404, content={ "message": "Користувач не знайдений"})

    #якщо користувача знайдено, відправляємо його
    return person

@app.post("/api/dentists")
def create_person(data = Body(), db: Session = Depends(get_db)):
    person = Person(name=data["name"], age=data["age"], experience=data["experience"], phoneNumber=data["phoneNumber"])
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.post("/api/dentists")
def create_dentist(data = Body(), db: Session = Depends(get_db)):
    dentist = Dentist(name=data["name"], age=data["age"], experience=data["experience"], phoneNumber=data["phoneNumber"])
    db.add(dentist)
    db.commit()
    db.refresh(dentist)
    return dentist


@app.put("/api/dentists")
def edit_person(data = Body(), db: Session = Depends(get_db)):
    # отримуємо користувача за id
    person = db.query(Person).filter(Person.id == data["id"]).first()
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку

    if person == None:
        return JSONResponse(status_code=404, content={ "message": "Користувач не знайдений"})

    # якщо користувач знайдений, змінюємо його дані і відправляємо назад клієнту
    person.age = data["age"]
    person.name = data["name"]
    db.commit()  # зберігаємо зміни
    db.refresh(person)
    return person

@app.delete("/api/dentists/{id}")
def delete_person(id, db: Session = Depends(get_db)):
    # отримуємо користувача за id
    person = db.query(Person).filter(Person.id == id).first()

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if person == None:
       return JSONResponse( status_code=404, content={ "message": "Користувач не знайдений"})

    # якщо користувача знайдено, видаляємо його
    db.delete(person) # видаляємо об'єкт
    db.commit() # зберігаємо зміни
    return person


@app.get("/dentalreg")
def dental_reg():
    return FileResponse(Path("public") / "dentistReg.html")
##################################################################################################################

@app.get("/patientreg")
def dental_reg():
    return FileResponse(Path("public") / "patientReg.html")



@app.get("/api/patients")
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

# 🔹 Отримати пацієнта за ID
@app.get("/api/patients/{id}")
def get_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Пацієнт не знайдений"})
    return patient

# 🔹 Додати нового пацієнта
@app.post("/api/patients")
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

# 🔹 Оновити дані пацієнта
@app.put("/api/patients")
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

# 🔹 Видалити пацієнта
@app.delete("/api/patients/{id}")
def delete_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Пацієнт не знайдений"})

    db.delete(patient)
    db.commit()
    return patient

##################################################################################################################

@app.get("/appointment")
def make_appointment():
    return FileResponse(Path("public") / "appointment.html")

@app.get("/api/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@app.get("/api/appointments/{id}")
def get_appointment(id: int, db: Session = Depends(get_db)):
    patient = db.query(Appointment).filter(Appointment.id == id).first()
    if not patient:
        return JSONResponse(status_code=404, content={"message": "Запис не знайдено"})
    return patient


@app.post("/api/appointments")
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


@app.put("/api/appointments")
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


@app.delete("/api/appointments/{id}")
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        return JSONResponse(status_code=404, content={"message": "Запис не знайдено"})

    db.delete(appointment)
    db.commit()
    return appointment