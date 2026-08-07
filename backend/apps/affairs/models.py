"""
Affairs Models
==============
Định nghĩa Data Model cho Module Công tác sinh viên.
Bao gồm Danh mục Khen thưởng/Kỷ luật.
"""
from django.db import models
from apps.core.models import TimeStampedModel

class RewardDisciplineCategory(TimeStampedModel):
    """
    Danh mục Khen thưởng & Kỷ luật.
    - Dùng để tham chiếu khi ra Quyết định khen thưởng/kỷ luật đối với sinh viên.
    """
    class TypeChoices(models.TextChoices):
        REWARD = 'REWARD', 'Khen thưởng'
        DISCIPLINE = 'DISCIPLINE', 'Kỷ luật'

    class LevelChoices(models.TextChoices):
        # Mức độ kỷ luật
        KHIEN_TRACH = 'KHIEN_TRACH', 'Khiển trách'
        CANH_CAO = 'CANH_CAO', 'Cảnh cáo'
        DINH_CHI = 'DINH_CHI', 'Đình chỉ học tập'
        BUOC_THOI_HOC = 'BUOC_THOI_HOC', 'Buộc thôi học'
        # Mức độ khen thưởng
        GIAY_KHEN = 'GIAY_KHEN', 'Giấy khen'
        BANG_KHEN = 'BANG_KHEN', 'Bằng khen'
        HOC_BONG = 'HOC_BONG', 'Học bổng'

    code = models.CharField(max_length=50, unique=True, help_text="Mã danh mục (VD: KT-01)")
    name = models.CharField(max_length=255, help_text="Tên danh mục (VD: Khiển trách)")
    type = models.CharField(max_length=50, choices=TypeChoices.choices, help_text="Phân loại: Khen thưởng hay Kỷ luật")
    level = models.CharField(max_length=50, choices=LevelChoices.choices, null=True, blank=True, help_text="Mức độ")
    training_points_impact = models.IntegerField(default=0, help_text="Điểm rèn luyện cộng thêm (nếu khen thưởng) hoặc trừ đi (nếu kỷ luật)")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'affairs_reward_discipline_categories'

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

class StudentRewardDiscipline(TimeStampedModel):
    """Bản ghi khen thưởng / kỷ luật của sinh viên"""
    class StatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', 'Nháp'
        PENDING = 'PENDING', 'Chờ duyệt'
        APPROVED = 'APPROVED', 'Đã duyệt'
        REVOKED = 'REVOKED', 'Đã thu hồi'

    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='reward_disciplines')
    category = models.ForeignKey(RewardDisciplineCategory, on_delete=models.PROTECT, related_name='records')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='reward_disciplines')
    
    decision_number = models.CharField(max_length=50, null=True, blank=True, help_text="Số quyết định")
    decision_date = models.DateField(null=True, blank=True, help_text="Ngày quyết định")
    reason = models.TextField(help_text="Lý do chi tiết")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    
    created_by = models.ForeignKey('identity.User', on_delete=models.SET_NULL, null=True, related_name='created_reward_disciplines')
    approved_by = models.ForeignKey('identity.User', on_delete=models.SET_NULL, null=True, related_name='approved_reward_disciplines')

    class Meta:
        db_table = 'affairs_student_reward_disciplines'

class TrainingScore(TimeStampedModel):
    """Điểm rèn luyện của sinh viên theo học kỳ"""
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='training_scores')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='training_scores')
    
    student_assessment = models.IntegerField(default=0, help_text="Điểm SV tự đánh giá")
    class_assessment = models.IntegerField(default=0, help_text="Điểm lớp đánh giá")
    faculty_assessment = models.IntegerField(default=0, help_text="Điểm khoa/trường đánh giá (Final)")
    
    status = models.CharField(max_length=20, choices=StudentRewardDiscipline.StatusChoices.choices, default=StudentRewardDiscipline.StatusChoices.DRAFT)
    
    class Meta:
        db_table = 'affairs_training_scores'
        unique_together = ('student', 'semester')

class Scholarship(TimeStampedModel):
    """Học bổng sinh viên"""
    class ScholarshipType(models.TextChoices):
        ACADEMIC = 'ACADEMIC', 'Khuyến khích học tập'
        SPONSOR = 'SPONSOR', 'Tài trợ doanh nghiệp'
        GOVERNMENT = 'GOVERNMENT', 'Hỗ trợ chính phủ'

    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='scholarships')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='scholarships')
    name = models.CharField(max_length=255, help_text="Tên học bổng")
    type = models.CharField(max_length=20, choices=ScholarshipType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Số tiền học bổng")
    status = models.CharField(max_length=20, choices=StudentRewardDiscipline.StatusChoices.choices, default=StudentRewardDiscipline.StatusChoices.PENDING)

    class Meta:
        db_table = 'affairs_scholarships'

class AdvisingSession(TimeStampedModel):
    """Lịch sử cố vấn học tập"""
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='advising_sessions')
    advisor = models.ForeignKey('hr.Staff', on_delete=models.CASCADE, related_name='advising_sessions', help_text="CVHT (Cán bộ/Giảng viên)")
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='advising_sessions')
    
    date = models.DateField()
    topic = models.CharField(max_length=255, help_text="Chủ đề tư vấn (VD: Cảnh báo học vụ, Kế hoạch học tập)")
    notes = models.TextField(help_text="Nội dung chi tiết buổi tư vấn")
    
    class Meta:
        db_table = 'affairs_advising_sessions'

class HealthInsurance(TimeStampedModel):
    """Bảo hiểm Y tế / Bảo hiểm Thân thể"""
    class TypeChoices(models.TextChoices):
        BHYT = 'BHYT', 'Bảo hiểm Y tế'
        BHTT = 'BHTT', 'Bảo hiểm Thân thể'
        
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='health_insurances')
    type = models.CharField(max_length=20, choices=TypeChoices.choices)
    provider = models.CharField(max_length=255, help_text="Nhà cung cấp (VD: BHXH Việt Nam)")
    insurance_number = models.CharField(max_length=50, help_text="Số thẻ bảo hiểm")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'affairs_health_insurances'

class Survey(TimeStampedModel):
    """Chiến dịch khảo sát"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='surveys')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'affairs_surveys'

class SurveyQuestion(TimeStampedModel):
    """Câu hỏi trong khảo sát"""
    class QuestionType(models.TextChoices):
        TEXT = 'TEXT', 'Văn bản'
        RATING = 'RATING', 'Đánh giá (1-5)'
        CHOICE = 'CHOICE', 'Trắc nghiệm'
        
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField(help_text="Nội dung câu hỏi")
    type = models.CharField(max_length=20, choices=QuestionType.choices)
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'affairs_survey_questions'
        ordering = ['order']

class SurveyResponse(TimeStampedModel):
    """Câu trả lời khảo sát của sinh viên"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='survey_responses')
    
    class Meta:
        db_table = 'affairs_survey_responses'
        unique_together = ('survey', 'student')

class SurveyAnswer(TimeStampedModel):
    """Chi tiết từng câu trả lời"""
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    
    text_answer = models.TextField(null=True, blank=True)
    rating_answer = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'affairs_survey_answers'

