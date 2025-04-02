from models.models import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, Path
from fastapi.responses import JSONResponse
from models.database import get_db
from fastapi import Depends, FastAPI, Body, HTTPException, Request
from security import *

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register")
def create_user(data=Body(), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == data["name"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач вже існує")
    user = User(
        username=data["name"],
        password=hash_password(data["password"]),

    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(request: Request, data=Body(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == data["username"]).first()
    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    request.session["user_id"] = user.id
    return JSONResponse({"message": "Вхід успішний!", "user": {"id": user.id, "username": user.username}})


@router.post("/logout/")
def logout(request: Request):
    request.session.clear()
    return JSONResponse({"message": "Вихід успішний!"})


@router.get("/protected/")
def protected_route(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Неавторизований доступ")

    user = db.query(User).filter(User.id == user_id).first()
    return {"message": f"Привіт, {user.username}! Ви увійшли в систему."}