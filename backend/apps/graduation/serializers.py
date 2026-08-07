from rest_framework import serializers
from .models import (
    GraduationCondition, GraduationSession, GraduationCandidate,
    Diploma, DefenseCouncil, Thesis
)
from apps.hr.serializers import StudentSerializer, LecturerSerializer
from apps.master_data.serializers import MajorReadSerializer, SemesterReadSerializer

class GraduationConditionSerializer(serializers.ModelSerializer):
    major_detail = MajorReadSerializer(source='major', read_only=True)
    
    class Meta:
        model = GraduationCondition
        fields = '__all__'

class GraduationSessionSerializer(serializers.ModelSerializer):
    semester_detail = SemesterReadSerializer(source='semester', read_only=True)
    
    class Meta:
        model = GraduationSession
        fields = '__all__'

class GraduationCandidateSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer(source='student', read_only=True)
    session_detail = GraduationSessionSerializer(source='session', read_only=True)
    
    class Meta:
        model = GraduationCandidate
        fields = '__all__'

class DiplomaSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer(source='student', read_only=True)
    
    class Meta:
        model = Diploma
        fields = '__all__'

class DefenseCouncilSerializer(serializers.ModelSerializer):
    president_detail = LecturerSerializer(source='president', read_only=True)
    secretary_detail = LecturerSerializer(source='secretary', read_only=True)
    
    class Meta:
        model = DefenseCouncil
        fields = '__all__'

class ThesisSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer(source='student', read_only=True)
    advisor_detail = LecturerSerializer(source='advisor', read_only=True)
    reviewer_detail = LecturerSerializer(source='reviewer', read_only=True)
    council_detail = DefenseCouncilSerializer(source='council', read_only=True)
    
    class Meta:
        model = Thesis
        fields = '__all__'
