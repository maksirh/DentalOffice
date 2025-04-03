from models.database import *
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from routers import dentist, patient, appointment, user
import auth
from security import require_role


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(dentist.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(user.router)
app.include_router(auth.router)
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
@require_role("admin")
def dental_reg(request: Request):
    return FileResponse(Path("public") / "dentistReg.html")

@app.get("/patientreg")
@require_role("admin")
def patient_reg(request: Request):
    return FileResponse(Path("public") / "patientReg.html")

@app.get("/appointment")
def make_appointment():
    return FileResponse(Path("public") / "appointment.html")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)