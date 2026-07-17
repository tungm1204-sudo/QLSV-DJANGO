"""
Affairs Serializers
===================
Chuyển đổi dữ liệu JSON <-> Model cho CTSV.
"""
from rest_framework import serializers
from .models import RewardDisciplineCategory

class RewardDisciplineCategorySerializer(serializers.ModelSerializer):
    """Serializer cho Khen thưởng/Kỷ luật."""
    class Meta:
        model = RewardDisciplineCategory
        fields = '__all__'
