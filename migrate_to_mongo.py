from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pymongo import MongoClient
from models.models import User, Dentist, Patient, Appointment, Review
from models.database import Base

# PostgreSQL
pg_engine = create_engine("postgresql://postgres:26041564@127.0.0.1:5432/dentalDB")
pg_session = Session(bind=pg_engine)

# MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["dental_mongo"]

# Мапа моделей - колекцій
model_collection_map = {
    User: "users",
    Dentist: "dentists",
    Patient: "patients",
    Appointment: "appointments",
    Review: "reviews"
}

# Міграція даних
for model, collection_name in model_collection_map.items():
    collection = mongo_db[collection_name]
    records = pg_session.query(model).all()
    documents = [
        {col.name: getattr(record, col.name) for col in model.__table__.columns}
        for record in records
    ]
    if documents:
        collection.insert_many(documents)

pg_session.close()
mongo_client.close()
print("Міграція з PostgreSQL у MongoDB завершена.")
