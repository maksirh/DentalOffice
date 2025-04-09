from models.models import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body
from models.database import get_db

router = APIRouter(prefix="/api/reviews", tags=["Patients"])

@router.get("/")
def get_review(db: Session = Depends(get_db)):
    return db.query(Review).all()

@router.post("/")
def leave_review(data=Body(), db: Session = Depends(get_db)):
    review = Review(
        review=data["review"],
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

