from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.database import Base
from models.models import User, Dentist, Patient, Appointment, Review

sqlite_engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})
pg_engine = create_engine("postgresql://postgres:26041564@127.0.0.1:5432/dentalDB")

Base.metadata.create_all(bind=pg_engine)
sqlite_session = Session(bind=sqlite_engine)
pg_session = Session(bind=pg_engine)

for model in (User, Dentist, Patient, Appointment, Review):
    records = sqlite_session.query(model).all()
    for record in records:
        data = {
            col.name: getattr(record, col.name)
            for col in model.__table__.columns
        }
        pg_session.merge(model(**data))

pg_session.commit()

print("Data migration complete!")
