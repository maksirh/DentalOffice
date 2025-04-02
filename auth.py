from models.models import *
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.database import get_db
from fastapi import Depends, HTTPException, Request

router = APIRouter(prefix="/auth")

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return JSONResponse({"message": "Вихід успішний!"})


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Неавторизований доступ")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Користувач не знайдений")

    return user


@router.get("/protected/")
def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Привіт, {user.username}! Ви увійшли в систему."}