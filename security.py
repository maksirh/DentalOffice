from passlib.context import CryptContext
from functools import wraps
from fastapi import HTTPException, Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def require_role(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            if request.session.get("role") != role:
                raise HTTPException(status_code=403, detail="Доступ заборонено")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator