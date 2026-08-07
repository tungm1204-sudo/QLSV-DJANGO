from rest_framework import serializers
from apps.affairs.models import (
    RewardDisciplineCategory, StudentRewardDiscipline,
    TrainingScore, Scholarship, AdvisingSession,
    HealthInsurance, Survey, SurveyQuestion, SurveyResponse, SurveyAnswer
)
from apps.hr.serializers import StudentSerializer, StaffSerializer

class RewardDisciplineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardDisciplineCategory
        fields = '__all__'

class StudentRewardDisciplineReadSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    category = RewardDisciplineCategorySerializer(read_only=True)
    
    class Meta:
        model = StudentRewardDiscipline
        fields = '__all__'

class StudentRewardDisciplineWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRewardDiscipline
        fields = '__all__'

class TrainingScoreSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    
    class Meta:
        model = TrainingScore
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    
    class Meta:
        model = Scholarship
        fields = '__all__'

class AdvisingSessionReadSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    advisor = StaffSerializer(read_only=True)
    
    class Meta:
        model = AdvisingSession
        fields = '__all__'

class AdvisingSessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvisingSession
        fields = '__all__'

class HealthInsuranceSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    
    class Meta:
        model = HealthInsurance
        fields = '__all__'

class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'

class SurveyReadSerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Survey
        fields = '__all__'

class SurveyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = ['question', 'text_answer', 'rating_answer']

class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(many=True)
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    
    class Meta:
        model = SurveyResponse
        fields = ['id', 'survey', 'student', 'student_code', 'created_at', 'answers']
        
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        response = SurveyResponse.objects.create(**validated_data)
        for answer_data in answers_data:
            SurveyAnswer.objects.create(response=response, **answer_data)
        return response
