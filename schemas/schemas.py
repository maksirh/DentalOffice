from pydantic import BaseModel
from fastapi import Path
from typing import Annotated

class User(BaseModel):
    id: int
    username: str
    password:  str


class Dentist(BaseModel):
    id: int
    name: str
    age: int
    experience: str
    phoneNumber: str


class Patient(BaseModel):
    id: int
    name: str
    age: int
    phoneNumber: str


class Appointment(BaseModel):
    id: int
    name: str
    age: int
    phoneNumber: str
    reason: str

