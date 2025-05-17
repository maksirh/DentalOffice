from fastapi import APIRouter, HTTPException, status, Body, Path
from bson import ObjectId
from mongodb import mongo_db
from schemas.schemas import PatientOut, PatientIn

router = APIRouter(prefix="/api/patients", tags=["Patients"])

def to_str_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientIn = Body(...)):
    data = patient.dict(by_alias=True, exclude={"id"})
    result = await mongo_db.patients.insert_one(data)
    new_doc = await mongo_db.patients.find_one({"_id": result.inserted_id})
    return PatientOut(**to_str_id(new_doc))

@router.get("/",response_model=list[PatientOut])
async def list_patients():
    cursor = mongo_db.patients.find()
    return [PatientOut(**to_str_id(doc)) async for doc in cursor]

@router.get("/{id}", response_model=PatientOut)
async def get_patient(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    doc = await mongo_db.patients.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Пацієнт не знайдений")
    return PatientOut(**doc)

@router.put("/{id}",response_model=PatientOut)
async def update_patient(id: str = Path(...),patient: PatientOut = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    data = patient.dict(by_alias=True, exclude={"id"})
    result = await mongo_db.patients.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Пацієнт не знайдений")
    updated = await mongo_db.patients.find_one({"_id": ObjectId(id)})
    return PatientOut(**updated)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_patient(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = await mongo_db.patients.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Пацієнт не знайдений")
