from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import csv
from io import StringIO

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Class(Base):
    __tablename__ = "classes"

    class_id = Column(String, primary_key=True, index=True)
    class_name = Column(String, index=True)
    advisor = Column(String)

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    birth_year = Column(Integer)
    major = Column(String)
    gpa = Column(Float)
    class_id = Column(String, ForeignKey("classes.class_id"))

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
def read_students(name: str = Query(None)):
    db = SessionLocal()
    try:
        all_students = db.query(Student).all()
        if name:
            all_students = [s for s in all_students if name.lower() in s.name.lower()]
        
        result = []
        for s in all_students:
            class_data = db.query(Class).filter(Class.class_id == s.class_id).first() if s.class_id else None
            result.append({
                "student_id": s.student_id,
                "name": s.name,
                "birth_year": s.birth_year,
                "major": s.major,
                "gpa": s.gpa,
                "class_id": s.class_id,
                "class_name": class_data.class_name if class_data else "",
                "advisor": class_data.advisor if class_data else ""
            })
        db.close()
        return result
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/classes")
def read_classes():
    db = SessionLocal()
    classes = db.query(Class).all()
    db.close()
    return classes

@app.post("/classes")
def create_class(class_data: dict):
    db = SessionLocal()
    db_class = Class(**class_data)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    db.close()
    return db_class

@app.get("/statistics")
def get_statistics():
    db = SessionLocal()
    total_students = db.query(Student).count()
    avg_gpa = db.query(func.avg(Student.gpa)).scalar() or 0
    major_counts = db.query(Student.major, func.count(Student.major)).group_by(Student.major).all()
    db.close()
    return {
        "total_students": total_students,
        "average_gpa": round(float(avg_gpa), 2),
        "students_by_major": {major: count for major, count in major_counts}
    }

@app.get("/export/csv")
def export_csv():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Student ID", "Name", "Birth Year", "Major", "GPA", "Class ID", "Class Name", "Advisor"])
        
        for s in students:
            class_data = db.query(Class).filter(Class.class_id == s.class_id).first() if s.class_id else None
            writer.writerow([
                s.student_id, 
                s.name, 
                s.birth_year, 
                s.major, 
                s.gpa, 
                s.class_id, 
                class_data.class_name if class_data else "", 
                class_data.advisor if class_data else ""
            ])
        
        db.close()
        return {"csv": output.getvalue()}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)