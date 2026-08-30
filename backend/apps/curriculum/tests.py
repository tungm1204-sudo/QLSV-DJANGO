from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.master_data.models import Major, Department, Cohort, CourseType
from apps.curriculum.models import Course, TrainingProgram, KnowledgeBlock, TrainingProgramCourse
from apps.curriculum.services import validate_knowledge_block_credits

class CurriculumRulesTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code="CNTT", name="Khoa CNTT")
        self.major = Major.objects.create(code="IT", name="IT", department=self.dept)
        self.cohort = Cohort.objects.create(code="K24", name="K24", admission_year=2024)
        
        self.tp1 = TrainingProgram.objects.create(
            code="TP-IT-K24", name="TP IT K24", major=self.major, cohort=self.cohort, total_credits=120
        )
        self.tp2 = TrainingProgram.objects.create(
            code="TP-SE-K24", name="TP SE K24", major=self.major, cohort=self.cohort, total_credits=120
        )
        
        self.course1 = Course.objects.create(code="C1", name="Course 1", credits=3, department=self.dept)
        self.course2 = Course.objects.create(code="C2", name="Course 2", credits=4, department=self.dept)

    def test_rule1_unique_block_code_per_tp(self):
        KnowledgeBlock.objects.create(training_program=self.tp1, code="BLK1", name="Block 1")
        
        # Cùng mã nhưng khác CTĐT thì OK
        KnowledgeBlock.objects.create(training_program=self.tp2, code="BLK1", name="Block 1")
        
        # Cùng mã và cùng CTĐT thì văng IntegrityError
        with self.assertRaises(IntegrityError):
            KnowledgeBlock.objects.create(training_program=self.tp1, code="BLK1", name="Block 1 Duplicate")

    def test_rule2_referential_integrity(self):
        block1 = KnowledgeBlock.objects.create(training_program=self.tp1, code="BLK1", name="Block 1")
        
        # Tạo TrainingProgramCourse hợp lệ
        tpc = TrainingProgramCourse(training_program=self.tp1, knowledge_block=block1, course=self.course1, semester_expected=1)
        tpc.full_clean()
        tpc.save()
        
        # Tạo TrainingProgramCourse không hợp lệ (TPC trỏ tp2 nhưng block thuộc tp1)
        tpc_invalid = TrainingProgramCourse(training_program=self.tp2, knowledge_block=block1, course=self.course2, semester_expected=1)
        with self.assertRaises(ValidationError) as ctx:
            tpc_invalid.full_clean()
        self.assertIn("knowledge_block", ctx.exception.message_dict)

    def test_rule3_mandatory_credits_validation(self):
        block = KnowledgeBlock.objects.create(training_program=self.tp1, code="BLK1", name="Block 1", mandatory_credits=6, elective_credits=3)
        
        # Khi chưa có môn nào
        with self.assertRaises(ValidationError):
            validate_knowledge_block_credits(block)
            
        # Thêm 1 môn bắt buộc 3 TC (Chưa đủ 6)
        TrainingProgramCourse.objects.create(training_program=self.tp1, knowledge_block=block, course=self.course1, semester_expected=1, is_mandatory=True)
        with self.assertRaises(ValidationError):
            validate_knowledge_block_credits(block)
            
        # Thêm 1 môn bắt buộc 4 TC (Tổng 7 > 6) -> Hợp lệ
        TrainingProgramCourse.objects.create(training_program=self.tp1, knowledge_block=block, course=self.course2, semester_expected=1, is_mandatory=True)
        self.assertTrue(validate_knowledge_block_credits(block))

    def test_rule4_semester_expected_min_1(self):
        block = KnowledgeBlock.objects.create(training_program=self.tp1, code="BLK1", name="Block 1")
        
        tpc_invalid = TrainingProgramCourse(training_program=self.tp1, knowledge_block=block, course=self.course1, semester_expected=0)
        with self.assertRaises(ValidationError) as ctx:
            tpc_invalid.full_clean()
        self.assertIn("semester_expected", ctx.exception.message_dict)
