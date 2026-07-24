"""
Affairs Serializers
"""
from rest_framework import serializers
from .models import RewardDisciplineCategory

class RewardDisciplineCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardDisciplineCategory
        fields = '__all__'

class RewardDisciplineCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardDisciplineCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

