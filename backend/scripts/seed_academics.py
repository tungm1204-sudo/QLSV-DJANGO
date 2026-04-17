import os
import sys
import django
import random
from datetime import date

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qlsv.settings')
django.setup()

from academics.models import Semester, Grade, Course, Classroom
from teachers.models import TeacherProfile

def seed():
    print("Seeding Academics...")
    
    # Semesters
    s1, _ = Semester.objects.get_or_create(
        name="Học kỳ 1", academic_year="2024-2025",
        defaults={"start_date": date(2024, 9, 1), "end_date": date(2025, 1, 15), "is_current": True}
    )
    s2, _ = Semester.objects.get_or_create(
        name="Học kỳ 2", academic_year="2024-2025",
        defaults={"start_date": date(2025, 2, 1), "end_date": date(2025, 6, 15), "is_current": False}
    )

    # Grades
    grades = []
    for g_name in ["Khối 10", "Khối 11", "Khối 12"]:
        g, _ = Grade.objects.get_or_create(name=g_name)
        grades.append(g)

    # Courses
    course_data = [
        ("Toán học", "MATH10", 4),
        ("Ngữ văn", "LIT10", 4),
        ("Tiếng Anh", "ENG10", 3),
        ("Vật lý", "PHYS10", 3),
        ("Hóa học", "CHEM10", 3),
    ]
    for name, code, credits in course_data:
        Course.objects.get_or_create(
            code=code,
            defaults={"name": name, "credits": credits, "grade": grades[0]}
        )

    # Classrooms
    teachers = list(TeacherProfile.objects.all())
    for i in range(1, 4):
        teacher = random.choice(teachers) if teachers else None
        Classroom.objects.get_or_create(
            name=f"10A{i}",
            semester=s1,
            defaults={"grade": grades[0], "homeroom_teacher": teacher}
        )

    print("Seeding completed!")

if __name__ == "__main__":
    seed()
