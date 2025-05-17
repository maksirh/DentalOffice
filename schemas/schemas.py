from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    role: str = "user"


class UserOut(BaseModel):
    id: str = Field(alias="_id")
    username: str
    role: str

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class PatientIn(BaseModel):
    name: str
    age: int
    phoneNumber: str

class PatientOut(PatientIn):
    id: str = Field(alias="_id")
    model_config = {"populate_by_name": True}

class DentistIn(BaseModel):
    name: str
    age: int
    experience: int
    phoneNumber: str

class DentistOut(DentistIn):
    id: str = Field(alias="_id")
    model_config = {"populate_by_name": True}

class AppointmentModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    age: int
    phoneNumber: str
    reason: str

    model_config = {
        "populate_by_name": True
    }

class ReviewModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    review: str

    model_config = {
        "populate_by_name": True
    }
