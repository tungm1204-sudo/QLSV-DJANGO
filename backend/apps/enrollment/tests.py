from django.test import TestCase
from django.utils import timezone
from apps.identity.models import User, Role
from apps.master_data.models import Major, Semester, Department
from apps.hr.models import Student
from apps.curriculum.models import Course, CourseOffering, TrainingPlan
from apps.enrollment.models import Enrollment
from apps.enrollment.services import enroll_student, change_course_offering, cancel_enrollment, approve_enrollment, lock_enrollment_list

class EnrollmentServiceTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='Student', permissions=[])
        self.user = User.objects.create(email='test@student.com', full_name='Test', role=self.role)
        self.department = Department.objects.create(code='D1', name='Dept')
        self.major = Major.objects.create(code='IT', name='IT', department=self.department)
        self.student = Student.objects.create(user=self.user, student_code='SV01', major=self.major)
        self.semester = Semester.objects.create(code='S1', start_date='2024-01-01', end_date='2024-06-01')
        self.course = Course.objects.create(code='C1', name='Course 1', credits=3, major=self.major)
        self.plan = TrainingPlan.objects.create(name='Plan 1', semester=self.semester, department=self.department)
        
        self.offering1 = CourseOffering.objects.create(
            training_plan=self.plan, course=self.course, semester=self.semester,
            status='OPEN', max_capacity=2
        )
        self.offering2 = CourseOffering.objects.create(
            training_plan=self.plan, course=self.course, semester=self.semester,
            status='OPEN', max_capacity=2
        )

    def test_enroll_student_success(self):
        enrollment = enroll_student(self.student, self.offering1.id, 'NORMAL', self.user, bypass_prerequisite=True)
        self.assertIsNotNone(enrollment)
        self.offering1.refresh_from_db()
        self.assertEqual(self.offering1.current_enrollment, 1)

    def test_enrollment_capacity_limit(self):
        self.offering1.current_enrollment = 2
        self.offering1.save()
        with self.assertRaises(Exception):
            enroll_student(self.student, self.offering1.id, 'NORMAL', self.user, bypass_prerequisite=True)
            
    def test_change_class(self):
        enrollment = enroll_student(self.student, self.offering1.id, 'NORMAL', self.user, bypass_prerequisite=True)
        self.offering1.refresh_from_db()
        self.assertEqual(self.offering1.current_enrollment, 1)
        
        new_enrollment = change_course_offering(enrollment.id, self.offering2.id, self.user, bypass_prerequisite=True)
        self.offering1.refresh_from_db()
        self.offering2.refresh_from_db()
        
        self.assertEqual(self.offering1.current_enrollment, 0)
        self.assertEqual(self.offering2.current_enrollment, 1)
        self.assertEqual(new_enrollment.course_offering, self.offering2)
