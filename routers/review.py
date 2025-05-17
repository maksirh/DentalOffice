from fastapi import APIRouter, HTTPException, status, Body
from mongodb import mongo_db
from schemas.schemas import ReviewModel

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

def to_str_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/", response_model=list[ReviewModel])
async def list_reviews():
    cursor = mongo_db.reviews.find()
    return [ReviewModel(**to_str_id(doc)) async for doc in cursor]

@router.post("/", response_model=ReviewModel, status_code=status.HTTP_201_CREATED)
async def leave_review(review: ReviewModel = Body(...)):
    data   = review.dict(by_alias=True, exclude={"id"})
    result = await mongo_db.reviews.insert_one(data)
    new_doc = await mongo_db.reviews.find_one({"_id": result.inserted_id})
    return ReviewModel(**new_doc)
