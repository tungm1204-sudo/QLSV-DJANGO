import uuid
from django.db import models
from apps.core.models import TimeStampedModel

class GraduationCondition(TimeStampedModel):
    """
    Điều kiện tốt nghiệp theo Ngành và Khóa
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    major = models.ForeignKey('master_data.Major', on_delete=models.CASCADE, related_name='graduation_conditions')
    cohort = models.CharField(max_length=50, null=True, blank=True, help_text="Khóa học (VD: K64). Nếu trống thì áp dụng chung.")
    
    total_credits_required = models.IntegerField(help_text="Tổng số tín chỉ yêu cầu")
    min_gpa = models.DecimalField(max_digits=4, decimal_places=2, help_text="GPA tối thiểu")
    required_certificates = models.JSONField(default=list, help_text="Danh sách loại chứng chỉ bắt buộc (VD: ['TOEIC', 'GDQP'])")
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'graduation_conditions'
        
    def __str__(self):
        return f"Điều kiện tốt nghiệp - {self.major.name} - {self.cohort or 'Chung'}"

class GraduationSession(TimeStampedModel):
    """
    Đợt xét tốt nghiệp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Tên đợt xét (VD: Đợt 1 năm 2024)")
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Nháp'),
        ('PROCESSING', 'Đang xử lý'),
        ('FINISHED', 'Đã hoàn tất')
    ], default='DRAFT')
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'graduation_sessions'
        
    def __str__(self):
        return self.name

class GraduationCandidate(TimeStampedModel):
    """
    Hồ sơ sinh viên trong đợt xét tốt nghiệp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(GraduationSession, on_delete=models.CASCADE, related_name='candidates')
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='graduation_records')
    
    # Kết quả xét
    total_credits = models.IntegerField(default=0)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    missing_conditions = models.JSONField(default=list, help_text="Các điều kiện còn thiếu")
    
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Chờ duyệt'),
        ('PASSED', 'Đủ điều kiện'),
        ('FAILED', 'Không đủ điều kiện'),
        ('APPROVED', 'Đã phê duyệt tốt nghiệp')
    ], default='PENDING')
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'graduation_candidates'
        unique_together = ('session', 'student')
        
    def __str__(self):
        return f"{self.student.student_code} - {self.session.name}"

class Diploma(TimeStampedModel):
    """
    Quản lý phôi bằng & cấp bằng tốt nghiệp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField('hr.Student', on_delete=models.CASCADE, related_name='diploma')
    candidate_record = models.OneToOneField(GraduationCandidate, on_delete=models.CASCADE, null=True, blank=True)
    
    diploma_number = models.CharField(max_length=100, unique=True, help_text="Số hiệu văn bằng")
    registry_number = models.CharField(max_length=100, unique=True, help_text="Số vào sổ cấp bằng")
    issue_date = models.DateField(help_text="Ngày ký cấp bằng")
    
    classification = models.CharField(max_length=50, help_text="Xếp loại tốt nghiệp (Xuất sắc, Giỏi, Khá, TB Khá, TB)")
    
    status = models.CharField(max_length=20, choices=[
        ('PRINTED', 'Đã in bằng'),
        ('ISSUED', 'Đã phát cho SV'),
        ('REVOKED', 'Bị thu hồi')
    ], default='PRINTED')
    
    received_by = models.CharField(max_length=255, null=True, blank=True, help_text="Người nhận (Sinh viên hoặc người được ủy quyền)")
    receive_date = models.DateField(null=True, blank=True, help_text="Ngày nhận bằng thực tế")
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'graduation_diplomas'
        
    def __str__(self):
        return self.diploma_number

class DefenseCouncil(TimeStampedModel):
    """
    Hội đồng bảo vệ đồ án tốt nghiệp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Tên hội đồng")
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE)
    major = models.ForeignKey('master_data.Major', on_delete=models.CASCADE)
    
    president = models.ForeignKey('hr.Lecturer', on_delete=models.PROTECT, related_name='council_presidents')
    secretary = models.ForeignKey('hr.Lecturer', on_delete=models.PROTECT, related_name='council_secretaries')
    
    defense_date = models.DateField()
    room = models.ForeignKey('master_data.Room', on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'graduation_defense_councils'
        
    def __str__(self):
        return self.name

class Thesis(TimeStampedModel):
    """
    Đồ án / Khóa luận tốt nghiệp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="Tên đề tài")
    student = models.OneToOneField('hr.Student', on_delete=models.CASCADE, related_name='thesis')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE)
    
    advisor = models.ForeignKey('hr.Lecturer', on_delete=models.PROTECT, related_name='advised_theses')
    reviewer = models.ForeignKey('hr.Lecturer', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_theses')
    council = models.ForeignKey(DefenseCouncil, on_delete=models.SET_NULL, null=True, blank=True, related_name='theses')
    
    advisor_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    reviewer_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    council_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    final_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=[
        ('REGISTERED', 'Đã đăng ký'),
        ('DEFENDING', 'Chờ bảo vệ'),
        ('PASSED', 'Bảo vệ thành công'),
        ('FAILED', 'Bảo vệ thất bại')
    ], default='REGISTERED')
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'graduation_theses'
        
    def __str__(self):
        return self.title
