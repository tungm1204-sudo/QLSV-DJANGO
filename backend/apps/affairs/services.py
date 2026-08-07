from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Sum

from apps.affairs.models import StudentRewardDiscipline, TrainingScore

@transaction.atomic
def create_reward_discipline(
    student_id: str,
    category_id: str,
    semester_id: str,
    reason: str,
    decision_number: str = None,
    decision_date=None,
    created_by_id: str = None
) -> StudentRewardDiscipline:
    record = StudentRewardDiscipline.objects.create(
        student_id=student_id,
        category_id=category_id,
        semester_id=semester_id,
        reason=reason,
        decision_number=decision_number,
        decision_date=decision_date,
        created_by_id=created_by_id
    )
    return record

@transaction.atomic
def approve_reward_discipline(record_id: str, approved_by_id: str) -> StudentRewardDiscipline:
    record = StudentRewardDiscipline.objects.select_related('category').get(id=record_id)
    if record.status != StudentRewardDiscipline.StatusChoices.PENDING and record.status != StudentRewardDiscipline.StatusChoices.DRAFT:
        raise ValidationError("Chỉ có thể duyệt bản ghi ở trạng thái Nháp hoặc Chờ duyệt.")
        
    record.status = StudentRewardDiscipline.StatusChoices.APPROVED
    record.approved_by_id = approved_by_id
    record.save()
    
    # Kích hoạt tính lại điểm rèn luyện của kỳ đó cho sinh viên này
    calculate_final_training_score(record.student_id, record.semester_id)
    
    return record

@transaction.atomic
def calculate_final_training_score(student_id: str, semester_id: str) -> TrainingScore:
    """Tính toán điểm rèn luyện cuối cùng dựa trên các điểm đánh giá và cộng trừ từ khen thưởng/kỷ luật"""
    score_record, _ = TrainingScore.objects.get_or_create(
        student_id=student_id,
        semester_id=semester_id
    )
    
    # Lấy điểm cộng/trừ từ các quyết định đã duyệt
    impact = StudentRewardDiscipline.objects.filter(
        student_id=student_id,
        semester_id=semester_id,
        status=StudentRewardDiscipline.StatusChoices.APPROVED
    ).aggregate(total_impact=Sum('category__training_points_impact'))['total_impact'] or 0
    
    # Ở đây faculty_assessment ban đầu được coi là điểm cơ bản (hoặc có thể lấy max(student, class) + impact)
    # Tùy thuộc vào quy chế. Ở đây ta giả sử faculty_assessment = class_assessment + impact
    # Đảm bảo điểm nằm trong [0, 100]
    base_score = score_record.class_assessment if score_record.class_assessment > 0 else score_record.student_assessment
    
    final = base_score + impact
    if final > 100: final = 100
    if final < 0: final = 0
    
    score_record.faculty_assessment = final
    score_record.save()
    return score_record
