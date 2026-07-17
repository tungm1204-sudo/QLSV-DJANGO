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
