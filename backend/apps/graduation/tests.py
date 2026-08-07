from django.test import TestCase
from apps.hr.models import Student, StudentCertificate
from apps.master_data.models import Major, Department, Cohort, Semester, EducationSystem, AdministrativeClass, AcademicYear
from apps.identity.models import User, Role
from apps.exams.models import StudentAcademicRecord
from apps.graduation.models import GraduationCondition
from apps.graduation.services import check_graduation_conditions

class GraduationServiceTests(TestCase):
    def setUp(self):
        # Create master data
        self.department = Department.objects.create(code='D01', name='CNTT')
        self.major = Major.objects.create(code='IT', name='Information Technology', department=self.department)
        self.cohort = Cohort.objects.create(code='K64', name='Khóa 64', admission_year=2019)
        self.academic_year = AcademicYear.objects.create(code='2023', name='2023-2024')
        self.semester = Semester.objects.create(code='20231', academic_year=self.academic_year, start_date='2023-09-01', end_date='2024-01-31')
        self.edu_sys = EducationSystem.objects.create(code='CQ', name='Chính quy')
        self.admin_class = AdministrativeClass.objects.create(code='IT1', name='Lớp CNTT 1', major=self.major, cohort=self.cohort, education_system=self.edu_sys)
        
        # Create student user
        self.role = Role.objects.create(name='STUDENT')
        self.user = User.objects.create_user(password='pwd', email='sv1@abc.com', role=self.role, full_name='SV1')
        self.student = Student.objects.create(
            user=self.user,
            student_code='SV001',
            administrative_class=self.admin_class,
            major=self.major,
            status='STUDYING'
        )
        
        # Create Graduation Condition
        self.condition = GraduationCondition.objects.create(
            major=self.major,
            cohort='K64',
            total_credits_required=120,
            min_gpa=2.5,
            required_certificates=['TOEIC', 'GDQP']
        )
        
    def test_check_graduation_conditions_eligible(self):
        # Create academic record
        StudentAcademicRecord.objects.create(
            student=self.student,
            semester=self.semester,
            cumulative_credits=125,
            cumulative_gpa_4=3.0
        )
        
        # Create certificates
        StudentCertificate.objects.create(
            student=self.student,
            certificate_type='TOEIC',
            certificate_name='TOEIC 650',
            issue_date='2023-01-01',
            status='APPROVED'
        )
        StudentCertificate.objects.create(
            student=self.student,
            certificate_type='GDQP',
            certificate_name='GDQP',
            issue_date='2020-01-01',
            status='APPROVED'
        )
        
        result = check_graduation_conditions(self.student.id)
        
        self.assertTrue(result['is_eligible'])
        self.assertEqual(len(result['missing_conditions']), 0)
        self.assertEqual(result['total_credits'], 125)

    def test_check_graduation_conditions_missing_credits(self):
        StudentAcademicRecord.objects.create(
            student=self.student,
            semester=self.semester,
            cumulative_credits=110,
            cumulative_gpa_4=3.0
        )
        
        # Has certificates
        StudentCertificate.objects.create(student=self.student, certificate_type='TOEIC', issue_date='2023-01-01', status='APPROVED')
        StudentCertificate.objects.create(student=self.student, certificate_type='GDQP', issue_date='2023-01-01', status='APPROVED')
        
        result = check_graduation_conditions(self.student.id)
        
        self.assertFalse(result['is_eligible'])
        self.assertTrue(any('Thiếu tín chỉ' in c for c in result['missing_conditions']))

    def test_check_graduation_conditions_missing_certificates(self):
        StudentAcademicRecord.objects.create(
            student=self.student,
            semester=self.semester,
            cumulative_credits=130,
            cumulative_gpa_4=3.0
        )
        
        # Only has TOEIC, missing GDQP
        StudentCertificate.objects.create(student=self.student, certificate_type='TOEIC', issue_date='2023-01-01', status='APPROVED')
        
        result = check_graduation_conditions(self.student.id)
        
        self.assertFalse(result['is_eligible'])
        self.assertTrue(any('GDQP' in c for c in result['missing_conditions']))
