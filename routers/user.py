from fastapi import APIRouter, HTTPException, status, Request, Body, Depends
from fastapi.responses import JSONResponse, FileResponse
from mongodb import mongo_db
from schemas.schemas import UserCreate, UserOut
from security import hash_password, verify_password
from bson import ObjectId

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate = Body(...)):
    existing = await mongo_db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    data = user.dict()
    data["password"] = hash_password(data["password"])
    result = await mongo_db.users.insert_one(data)
    new_user = await mongo_db.users.find_one({"_id": result.inserted_id})
    return UserOut(**new_user)

@router.post("/login")
async def login(request: Request, credentials: UserCreate = Body(...)):
    user = await mongo_db.users.find_one({"username": credentials.username})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # set session
    request.session["user_id"] = str(user["_id"])
    request.session["role"] = user.get("role", "user")
    return JSONResponse({
        "message": "Login successful",
        "user": {"id": str(user["_id"]), "username": user["username"], "role": user.get("role", "user")}
    })

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return JSONResponse({"message": "Logout successful"})

async def get_current_user(request: Request) -> dict:

    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user id in session"
        )

    user_doc = await mongo_db.users.find_one(
        {"_id": ObjectId(user_id)}
    )
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_doc["_id"] = str(user_doc["_id"])
    return user_doc

@router.get("/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/profile")
async def profile():
    return FileResponse("public/profile.html")

@router.get("/{id}", response_model=UserOut)
async def get_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    user = await mongo_db.users.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)