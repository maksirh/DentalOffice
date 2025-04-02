from models.models import *
from models.database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from routers import dentist, patient, appointment, user


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(dentist.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(user.router)
app.mount("/public", StaticFiles(directory="public"), name="public")
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")


@app.get("/")
def main():
    return FileResponse("public/home.html")

@app.get("/login")
def login():
    return FileResponse(Path("public") / "login.html")

@app.get("/register")
def register():
    return FileResponse(Path("public") / "register.html")

@app.get("/dentalreg")
def dental_reg():
    return FileResponse(Path("public") / "dentistReg.html")

@app.get("/patientreg")
def dental_reg():
    return FileResponse(Path("public") / "patientReg.html")

@app.get("/appointment")
def make_appointment():
    return FileResponse(Path("public") / "appointment.html")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)