from sqlalchemy import Column, Integer, String
from models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")


class Dentist(Base):
    __tablename__ = "dentists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )
    experience = Column(Integer, )
    phoneNumber = Column(String)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )
    phoneNumber = Column(String)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )
    phoneNumber = Column(String)
    reason = Column(String)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    review = Column(String)