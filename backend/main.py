from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    birth_year = Column(Integer)
    major = Column(String)
    gpa = Column(Float)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students")
def read_students():
    db = SessionLocal()
    students = db.query(Student).all()
    db.close()
    return students

@app.post("/students")
def create_student(student: dict):
    db = SessionLocal()
    db_student = Student(**student)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    db.close()
    return db_student

@app.put("/students/{student_id}")
def update_student(student_id: str, student: dict):
    db = SessionLocal()
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if not db_student:
        db.close()
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    db.close()
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    db = SessionLocal()
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if not db_student:
        db.close()
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    db.close()
    return {"message": "Student deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)