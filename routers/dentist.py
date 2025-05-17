from fastapi import APIRouter, HTTPException, status, Body, Path
from mongodb import mongo_db
from schemas.schemas import DentistIn, DentistOut
from bson import ObjectId

router = APIRouter(prefix="/api/dentists", tags=["Dentists"])

def to_str_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=DentistOut, status_code=status.HTTP_201_CREATED,)
async def create_dentist(dentist: DentistIn = Body(...)):
    data = dentist.dict(by_alias=True, exclude_none=True, exclude={"_id"})
    result = await mongo_db.dentists.insert_one(data)
    new_doc = await mongo_db.dentists.find_one({"_id": result.inserted_id})
    return DentistOut(**to_str_id(new_doc))


@router.get("/", response_model=list[DentistOut])
async def list_dentists():
    cursor = mongo_db.dentists.find({})
    return [DentistOut(**to_str_id(doc)) async for doc in cursor]

@router.get("/{id}", response_model=DentistOut)
async def get_dentist(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    doc = await mongo_db.dentists.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(404, "Дантист не знайдений")
    return DentistOut(**to_str_id(doc))

@router.put("/{id}", response_model=DentistOut)
async def update_dentist(
    id: str = Path(..., title="Dentist ID"),
    dentist: DentistIn = Body(...)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")

    data = dentist.dict(exclude_unset=True, by_alias=True)

    if not data:
        raise HTTPException(400, "Нічого оновлювати")

    result = await mongo_db.dentists.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Дантист не знайдений")

    updated = await mongo_db.dentists.find_one({"_id": ObjectId(id)})
    return DentistOut(**to_str_id(updated))

@router.delete("/{id}", status_code=204)
async def delete_dentist(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    result = await mongo_db.dentists.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Дантист не знайдений")