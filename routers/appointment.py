from fastapi import APIRouter, HTTPException, status, Body, Path
from mongodb import mongo_db
from schemas.schemas import AppointmentModel
from bson import ObjectId

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

def to_str_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

@router.post(
    "/",
    response_model=AppointmentModel,
    status_code=status.HTTP_201_CREATED
)
async def create_appointment(appointment: AppointmentModel = Body(...)):
    data = appointment.dict(by_alias=True, exclude={"id"})
    result = await mongo_db.appointments.insert_one(data)
    new_doc = await mongo_db.appointments.find_one({"_id": result.inserted_id})
    return AppointmentModel(**new_doc)

@router.get(
    "/",
    response_model=list[AppointmentModel]
)
async def list_appointments():
    cursor = mongo_db.appointments.find()
    return [AppointmentModel(**to_str_id(doc)) async for doc in cursor]

@router.get(
    "/{id}",
    response_model=AppointmentModel
)
async def get_appointment(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    doc = await mongo_db.appointments.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return AppointmentModel(**doc)

@router.put(
    "/{id}",
    response_model=AppointmentModel
)
async def update_appointment(
    id: str = Path(...),
    appointment: AppointmentModel = Body(...)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    data = appointment.dict(by_alias=True, exclude={"id"})
    result = await mongo_db.appointments.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Appointment not found")
    updated = await mongo_db.appointments.find_one({"_id": ObjectId(id)})
    return AppointmentModel(**updated)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_appointment(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    result = await mongo_db.appointments.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Appointment not found")
