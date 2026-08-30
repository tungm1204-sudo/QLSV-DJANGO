from unittest.mock import patch
from types import SimpleNamespace

from django.test import TestCase

from apps.identity.models import User, Role
from apps.master_data.models import Major, Semester, Department, Campus, Building, Room, CourseType, Cohort, AcademicYear
from apps.hr.models import Student
from apps.curriculum.models import Course, CourseOffering, TrainingPlan
from apps.enrollment.models import Enrollment
from apps.enrollment import selectors
from apps.enrollment.services import enroll_student, change_course_offering, cancel_enrollment, approve_enrollment, lock_enrollment_list
from apps.enrollment.views import StudentEnrollmentViewSet

class EnrollmentServiceTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='Student', permissions=[])
        self.user = User.objects.create(email='test@student.com', full_name='Test', role=self.role)
        self.department = Department.objects.create(code='D1', name='Dept')
        self.campus = Campus.objects.create(code='CAMPUS1', name='Campus 1')
        self.building = Building.objects.create(code='B1', name='Building 1', campus=self.campus, floor_count=2, is_active=True)
        self.room = Room.objects.create(code='R1', name='Room 1', building=self.building, floor=1, type='THEORY', capacity=50, facilities={}, status='ACTIVE')
        self.major = Major.objects.create(code='IT', name='IT', department=self.department)
        self.student = Student.objects.create(user=self.user, student_code='SV01', major=self.major)
        self.semester = Semester.objects.create(code='S1', start_date='2024-01-01', end_date='2024-06-01')

        self.course_type = CourseType.objects.create(code='CT1', name='Type 1')
        self.course = Course.objects.create(code='C1', name='Course 1', credits=3, department=self.department)
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

    def test_get_student_schedule_includes_approved_enrollments(self):
        enroll_student(self.student, self.offering1.id, 'NORMAL', self.user, bypass_prerequisite=True)
        self.offering1.schedules.create(day_of_week='MONDAY', start_period=1, end_period=3, room=self.room)

        schedules = selectors.get_student_schedule(self.student.id)

        self.assertEqual(len(schedules), 1)

    def test_student_register_does_not_allow_bypass_for_non_staff(self):
        request = SimpleNamespace(
            user=SimpleNamespace(id='user-1', is_staff=False, is_authenticated=True, student_profile=self.student),
            data={'course_offering_id': str(self.offering1.id), 'enrollment_type': 'NORMAL', 'bypass_prerequisite': True}
        )

        view = StudentEnrollmentViewSet()
        with patch('apps.enrollment.views.services.enroll_student') as mock_enroll:
            mock_enroll.return_value = SimpleNamespace(id='enr-1')
            view.register(request)

        self.assertTrue(mock_enroll.called)
        self.assertFalse(mock_enroll.call_args.kwargs['bypass_prerequisite'])
