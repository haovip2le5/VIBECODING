from main import engine, Base, SessionLocal, Student, Class

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add sample classes
classes = [
    Class(class_id="C01", class_name="Khoa học máy tính 1", advisor="Nguyen Van A"),
    Class(class_id="C02", class_name="Kỹ thuật phần mềm", advisor="Tran Van B"),
    Class(class_id="C03", class_name="Công nghệ thông tin", advisor="Le Van C"),
]

for cls in classes:
    db.add(cls)

db.commit()

# Add sample students
students = [
    Student(student_id="1231234", name="Hao", birth_year=2005, major="Computer Science", gpa=3.2, class_id="C01"),
    Student(student_id="1231235", name="Linh", birth_year=2005, major="Computer Science", gpa=3.5, class_id="C01"),
    Student(student_id="1231236", name="Duc", birth_year=2005, major="Software Engineering", gpa=3.8, class_id="C02"),
    Student(student_id="1231237", name="An", birth_year=2004, major="Information Technology", gpa=3.3, class_id="C03"),
    Student(student_id="1231238", name="Binh", birth_year=2004, major="Computer Science", gpa=3.6, class_id="C01"),
    Student(student_id="1231239", name="Chi", birth_year=2005, major="Software Engineering", gpa=3.9, class_id="C02"),
    Student(student_id="1231240", name="Dung", birth_year=2004, major="Information Technology", gpa=3.4, class_id="C03"),
    Student(student_id="1231241", name="Em", birth_year=2005, major="Computer Science", gpa=3.7, class_id="C01"),
]

for student in students:
    db.add(student)

db.commit()
db.close()

print("✅ Dữ liệu mẫu đã được thêm vào database!")
